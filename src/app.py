import datetime
import json
import os
import random
import urllib.error
import urllib.request
import uuid

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from .config import (
    FRONTEND_DIR, TEMPLATE_DIR, STATIC_DIR,
    ADMIN_USERNAME, ADMIN_PASSWORD,
    DEFAULT_COURSES, DEFAULT_EVENTS
)
from .database import (
    get_db, initialize_db,
    list_event_documents, find_event, replace_event,
    list_registration_documents, list_lead_documents
)
from .auth import encode_token, current_user, admin_user, require_admin
from .scoring import score, predict_admission

def create_app():
    app = Flask(
        __name__,
        static_folder=FRONTEND_DIR,
        static_url_path="",
        template_folder=TEMPLATE_DIR
    )
    CORS(app)

    initialize_db()

    def request_data():
        return request.get_json(silent=True) or {}

    def validate_event(data):
        required = ("type", "date", "title", "description", "place", "format")
        missing = [field for field in required if not isinstance(data.get(field), str) or not data[field].strip()]
        if missing:
            return f"Please provide: {', '.join(missing)}."
        if data["type"] not in ("Conference", "Workshop", "Seminar"):
            return "Event type must be Conference, Workshop or Seminar."
        if len(data["title"].strip()) > 160 or len(data["description"].strip()) > 1000:
            return "Event title must be at most 160 characters and description at most 1,000 characters."
        image = data.get("image", "")
        if not isinstance(image, str):
            return "Event image must be a URL or path."
        if image.strip() and not image.strip().startswith(("https://", "http://", "images/")):
            return "Event image URL must start with http://, https://, or images/."
        try:
            datetime.date.fromisoformat(data["date"])
        except ValueError:
            return "Date must use YYYY-MM-DD format."
        return None

    # Static page routes
    @app.route("/")
    def home():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.route("/admissions")
    def admissions_view():
        return send_from_directory(FRONTEND_DIR, "admissions.html")

    @app.route("/courses")
    def courses_view():
        return send_from_directory(FRONTEND_DIR, "courses.html")

    # Auth routes
    @app.route("/register", methods=["POST"])
    def register():
        data = request_data()
        name = str(data.get("name", "")).strip()
        username = str(data.get("username", "")).strip().lower()
        email = str(data.get("email", "")).strip().lower()
        phone = str(data.get("phone", "")).strip()
        password = str(data.get("password", ""))
        role = str(data.get("role", "student")).strip().lower()
        if role not in ("student", "admin"):
            role = "student"

        if not name or not username or not email or not password:
            return jsonify({"error": "Please provide your Full Name, Username, Email, and Password."}), 400

        if len(username) < 3 or len(username) > 30:
            return jsonify({"error": "Username must be between 3 and 30 characters."}), 400

        if "@" not in email or "." not in email:
            return jsonify({"error": "Please provide a valid email address."}), 400

        if len(password) < 4:
            return jsonify({"error": "Password must be at least 4 characters long."}), 400

        with get_db() as connection:
            existing = connection.execute(
                "SELECT id, username, email FROM users WHERE lower(username) = ? OR lower(email) = ?",
                (username, email)
            ).fetchone()
            if existing:
                if existing["username"].lower() == username:
                    return jsonify({"error": f"Username '{username}' is already taken. Please choose another."}), 409
                return jsonify({"error": f"An account with email '{email}' already exists. Please sign in."}), 409

            password_hash = generate_password_hash(password)
            created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
            cursor = connection.execute(
                "INSERT INTO users (username, email, phone, name, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (username, email, phone, name, password_hash, role, created_at)
            )
            user_id = cursor.lastrowid

        token = encode_token({
            "user": username,
            "user_id": user_id,
            "role": role,
            "name": name,
            "email": email
        })

        return jsonify({
            "status": "Registered",
            "message": "Registration successful! Welcome to CUTM.",
            "token": token,
            "user": {
                "id": user_id,
                "name": name,
                "username": username,
                "email": email,
                "phone": phone,
                "role": role
            }
        }), 201

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return send_from_directory(FRONTEND_DIR, "login.html")
        data = request_data()
        login_id = str(data.get("username", "")).strip().lower()
        password = str(data.get("password", ""))

        if not login_id or not password:
            return jsonify({"error": "Username/Email and password are required."}), 400

        with get_db() as connection:
            user_row = connection.execute(
                "SELECT * FROM users WHERE lower(username) = ? OR lower(email) = ?", (login_id, login_id)
            ).fetchone()

        if user_row:
            if check_password_hash(user_row["password_hash"], password):
                token = encode_token({
                    "user": user_row["username"],
                    "user_id": user_row["id"],
                    "role": user_row["role"],
                    "name": user_row["name"],
                    "email": user_row["email"]
                })
                return jsonify({
                    "token": token,
                    "user": {
                        "id": user_row["id"],
                        "username": user_row["username"],
                        "name": user_row["name"],
                        "email": user_row["email"],
                        "role": user_row["role"]
                    }
                })
            else:
                return jsonify({"error": "Incorrect password. Please try again."}), 401

        if login_id == ADMIN_USERNAME.lower() and password == ADMIN_PASSWORD:
            token = encode_token({
                "user": "admin",
                "role": "admin",
                "name": "CUTM Administrator"
            })
            return jsonify({
                "token": token,
                "user": {
                    "username": "admin",
                    "name": "CUTM Administrator",
                    "role": "admin"
                }
            })

        return jsonify({"error": "No account found with this username or email. Please register."}), 401

    @app.route("/api/me", methods=["GET"])
    def me():
        payload = current_user()
        if not payload:
            return jsonify({"authenticated": False}), 401
        return jsonify({"authenticated": True, "user": payload})

    # Courses API
    @app.route("/api/courses", methods=["GET"])
    def get_courses_api():
        return jsonify(DEFAULT_COURSES)

    # Lead & Admission routes
    @app.route("/lead", methods=["POST"])
    def lead():
        data = request_data()
        if not data.get("phone") and not data.get("email"):
            return jsonify({"error": "Phone number or email is required."}), 400

        data["score"] = score(data)
        if "created_at" not in data:
            data["created_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if "ref_id" not in data:
            data["ref_id"] = f"CUTM-{random.randint(100000, 999999)}"
        if "status" not in data:
            data["status"] = "New"

        name = data.get("name", "Student")
        phone = data.get("phone", "N/A")
        email = data.get("email", "N/A")
        course = data.get("course", "General")
        marks = data.get("marks", "N/A")
        ref_id = data.get("ref_id")
        city = data.get("city", "")
        state = data.get("state", "")
        location = f"{city}, {state}".strip(", ") or "N/A"

        print("\n" + "=" * 65, flush=True)
        print(">>> [NEW ADMISSION APPLICATION RECEIVED!]", flush=True)
        print(f"Ref ID   : {ref_id}", flush=True)
        print(f"Student  : {name}", flush=True)
        print(f"Contact  : Phone: {phone} | Email: {email}", flush=True)
        print(f"Course   : {course} (Marks: {marks}%)", flush=True)
        print(f"Location : {location}", flush=True)
        print(f"Score    : {data.get('score')} | Date: {data.get('created_at')}", flush=True)
        print("=" * 65 + "\n", flush=True)

        with get_db() as connection:
            cursor = connection.execute("INSERT INTO leads (data) VALUES (?)", (json.dumps(data),))
            lead_id = cursor.lastrowid
        return jsonify({
            "status": "Saved",
            "id": lead_id,
            "ref_id": ref_id,
            "score": data["score"],
            "lead": data
        }), 201

    @app.route("/api/application-status/<query>", methods=["GET"])
    def application_status(query):
        query = query.strip()
        with get_db() as connection:
            rows = connection.execute("SELECT data FROM leads ORDER BY id DESC").fetchall()
        for row in rows:
            lead_data = json.loads(row["data"])
            if lead_data.get("ref_id", "").upper() == query.upper() or lead_data.get("phone", "") == query:
                return jsonify({
                    "found": True,
                    "ref_id": lead_data.get("ref_id"),
                    "name": lead_data.get("name"),
                    "course": lead_data.get("course"),
                    "department": lead_data.get("department"),
                    "marks": lead_data.get("marks"),
                    "score": lead_data.get("score"),
                    "status": lead_data.get("status", "Under Verification"),
                    "created_at": lead_data.get("created_at")
                })
        return jsonify({"found": False, "error": "No application found for this Reference ID or Phone number."}), 404

    @app.route("/leads")
    def get_leads():
        unauthorized = require_admin()
        if unauthorized:
            return unauthorized
        return jsonify(list_lead_documents())

    @app.route("/delete/<phone>", methods=["DELETE"])
    def delete_lead(phone):
        unauthorized = require_admin()
        if unauthorized:
            return unauthorized
        with get_db() as connection:
            rows = connection.execute("SELECT id, data FROM leads").fetchall()
            ids = [
                row["id"] for row in rows
                if json.loads(row["data"]).get("phone") == phone
            ]
            connection.executemany("DELETE FROM leads WHERE id = ?", [(item,) for item in ids])
        return jsonify({"status": "Deleted"})

    @app.route("/update/<phone>", methods=["PUT"])
    def update_lead(phone):
        unauthorized = require_admin()
        if unauthorized:
            return unauthorized
        updates = request_data()
        with get_db() as connection:
            rows = connection.execute("SELECT id, data FROM leads").fetchall()
            for row in rows:
                lead_document = json.loads(row["data"])
                if lead_document.get("phone") == phone:
                    lead_document.update(updates)
                    connection.execute(
                        "UPDATE leads SET data = ? WHERE id = ?",
                        (json.dumps(lead_document), row["id"]),
                    )
        return jsonify({"status": "Updated"})

    @app.route("/predict", methods=["POST"])
    def predict_endpoint():
        data = request_data()
        try:
            marks = float(data.get("marks", 0))
        except (TypeError, ValueError):
            return jsonify({"error": "Marks must be a number."}), 400

        course = data.get("course", "General")
        result = predict_admission(marks, course)
        return jsonify(result)

    @app.route("/stats")
    def stats():
        unauthorized = require_admin()
        if unauthorized:
            return unauthorized
        lead_documents = list_lead_documents()
        course_totals = {}
        for lead_document in lead_documents:
            course = lead_document.get("course") or "Unspecified"
            course_totals[course] = course_totals.get(course, 0) + 1
        return jsonify({
            "total": len(lead_documents),
            "courses": [{"_id": course, "count": count} for course, count in course_totals.items()],
        })

    # Events API
    @app.route("/events", methods=["GET"])
    def list_events():
        return jsonify(list_event_documents())

    @app.route("/events", methods=["POST"])
    def create_event():
        unauthorized = require_admin()
        if unauthorized:
            return unauthorized
        data = request_data()
        error = validate_event(data)
        if error:
            return jsonify({"error": error}), 400
        event = {field: data[field].strip() for field in ("type", "date", "title", "description", "place", "format")}
        event.update({"id": str(uuid.uuid4()), "image": data.get("image", "").strip()})
        replace_event(event)
        return jsonify({"event": event}), 201

    @app.route("/events/<event_id>", methods=["PUT", "DELETE"])
    def update_event(event_id):
        unauthorized = require_admin()
        if unauthorized:
            return unauthorized
        if request.method == "DELETE":
            with get_db() as connection:
                result = connection.execute("DELETE FROM events WHERE id = ?", (event_id,))
            if result.rowcount == 0:
                return jsonify({"error": "Event not found or is a built-in sample event."}), 404
            return jsonify({"status": "Deleted"})

        data = request_data()
        error = validate_event(data)
        if error:
            return jsonify({"error": error}), 400
        event = {field: data[field].strip() for field in ("type", "date", "title", "description", "place", "format")}
        event.update({"id": event_id, "image": data.get("image", "").strip()})
        replace_event(event)
        return jsonify({"event": event})

    @app.route("/registrations", methods=["POST", "GET"])
    def registrations_route():
        if request.method == "GET":
            unauthorized = require_admin()
            if unauthorized:
                return unauthorized
            return jsonify(list_registration_documents())

        data = request_data()
        required = ("name", "email", "phone", "event_id")
        if any(not isinstance(data.get(field), str) or not data[field].strip() for field in required):
            return jsonify({"error": "Name, email, phone and event are required."}), 400
        email = data["email"].strip().lower()
        name = data["name"].strip()
        phone = "".join(character for character in data["phone"] if character.isdigit())
        if len(name) > 100 or len(email) > 254 or len(data["phone"]) > 20:
            return jsonify({"error": "Name, email or phone exceeds the allowed length."}), 400
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            return jsonify({"error": "Please provide a valid email address."}), 400
        if len(phone) < 10 or len(phone) > 15:
            return jsonify({"error": "Please provide a valid phone number."}), 400
        selected_event = find_event(data["event_id"])
        if not selected_event:
            return jsonify({"error": "Selected event was not found."}), 404

        registration = {
            "id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "phone": phone,
            "event_id": selected_event["id"],
            "event_title": selected_event["title"],
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        with get_db() as connection:
            connection.execute(
                "INSERT INTO event_registrations (id, data) VALUES (?, ?)",
                (registration["id"], json.dumps(registration)),
            )
        return jsonify({"status": "Registered", "registration_id": registration["id"]}), 201

    @app.route("/registrations/<registration_id>", methods=["DELETE"])
    def delete_registration(registration_id):
        unauthorized = require_admin()
        if unauthorized:
            return unauthorized
        with get_db() as connection:
            result = connection.execute(
                "DELETE FROM event_registrations WHERE id = ?", (registration_id,)
            )
        if result.rowcount == 0:
            return jsonify({"error": "Registration not found."}), 404
        return jsonify({"status": "Deleted"})

    # Chatbot route
    @app.route("/chat", methods=["POST"])
    def chat():
        data = request_data()
        message = data.get("message", "")
        if not isinstance(message, str) or not message.strip():
            return jsonify({"error": "Please provide a message."}), 400
        message = message.strip()
        if len(message) > 2000:
            return jsonify({"error": "Messages must be 2,000 characters or fewer."}), 400

        msg = message.lower()
        replies = {
            "cse": "B.Tech Computer Science & Engineering (CSE) offers advanced training in AI, Machine Learning, Cloud Computing, Cyber Security, and Web Technologies with high placement rates.",
            "computer": "B.Tech CSE covers Artificial Intelligence, Data Science, Cloud Systems, and Full-Stack Development. Check the Courses or Admissions page to apply.",
            "ece": "B.Tech Electronics & Communication Engineering (ECE) specializes in VLSI Design, Embedded Systems, IoT, Robotics, and 5G Communications.",
            "machnical": "B.Tech Mechanical Engineering focuses on Robotics, CAD/CAM/CAE, EV Technology, Automation, and Advanced Manufacturing with modern lab infrastructure.",
            "mechanical": "B.Tech Mechanical Engineering focuses on Robotics, CAD/CAM/CAE, EV Technology, Automation, and Advanced Manufacturing with modern lab infrastructure.",
            "civil": "B.Tech Civil Engineering covers Smart Cities, Structural Analysis, Green Building Design, Total Station Surveying, and Infrastructure Engineering.",
            "b.tech": "We offer B.Tech degrees in 4 high-demand engineering branches: CSE, ECE, Mechanical, and Civil Engineering (4 Years duration, 10+2 PCM with min 50%).",
            "btech": "We offer B.Tech degrees in 4 high-demand engineering branches: CSE, ECE, Mechanical, and Civil Engineering (4 Years duration, 10+2 PCM with min 50%).",
            "engineering": "Our Engineering faculty offers B.Tech in CSE, ECE, Mechanical, and Civil, as well as Diploma in Engineering (Polytechnic).",
            "diploma": "Diploma (Polytechnic) is a 3-year practical program (2-year lateral entry) in CSE, Mechanical, Civil, and Electrical for 10th or 12th/ITI students.",
            "polytechnic": "Diploma (Polytechnic) is a 3-year career-focused engineering program after 10th or 10+2/ITI with hands-on workshop training.",
            "agriculure": "B.Sc. (Hons.) Agriculture is a 4-year degree covering Agronomy, Precision Farming, Soil Science, Horticulture, and Agri-Business on dedicated research farms.",
            "agriculture": "B.Sc. (Hons.) Agriculture is a 4-year degree covering Agronomy, Precision Farming, Soil Science, Horticulture, and Agri-Business on dedicated research farms.",
            "bba": "BBA (Bachelor of Business Administration) is a 3-year undergraduate program focusing on Marketing, Finance, HR, Entrepreneurship, and Business Analytics.",
            "nursing": "B.Sc. Nursing is an INC-approved 4-year healthcare program with clinical hospital rotations, simulation labs, and global career opportunities.",
            "bsc nursing": "B.Sc. Nursing is an INC-approved 4-year healthcare program with clinical hospital rotations, simulation labs, and global career opportunities.",
            "admission": "Admissions 2026-2027 are OPEN for B.Tech (CSE, ECE, Mechanical, Civil), Diploma, Agriculture, BBA, and B.Sc Nursing. Apply online on our Admissions page or call 1800-123-CUTM.",
            "apply": "You can apply online right now! Head to the Admissions page, choose your department and course, and submit your application with instant eligibility check.",
            "fee": "Annual fees: B.Tech CSE: ₹1,10,000 | B.Tech ECE: ₹95,000 | Mechanical: ₹90,000 | Civil: ₹85,000 | Diploma: ₹45,000 | Agriculture: ₹80,000 | BBA: ₹65,000 | B.Sc Nursing: ₹1,05,000.",
            "fees": "Annual fees: B.Tech CSE: ₹1,10,000 | B.Tech ECE: ₹95,000 | Mechanical: ₹90,000 | Civil: ₹85,000 | Diploma: ₹45,000 | Agriculture: ₹80,000 | BBA: ₹65,000 | B.Sc Nursing: ₹1,05,000.",
            "scholarship": "We offer Chancellor Merit Scholarships: up to 100% tuition waiver for 90%+ marks, and 25%-50% for 75-89% marks, plus sports and defense quotas.",
            "eligibility": "Eligibility: B.Tech requires 10+2 PCM (50%); B.Sc Nursing requires 10+2 PCB (45-50%); B.Sc Agriculture requires 10+2 PCB/PCM (50%); BBA requires 10+2 (45%); Diploma requires 10th (45%).",
            "register": "Select Register on an event card or visit login.html to create your student or staff portal account.",
            "contact": "You can reach our CUTM admissions desk at admissions@cutm.ac.in or helpline 1800-123-CUTM.",
            "course": "Explore our departments: Engineering (B.Tech CSE, ECE, Mech, Civil), Diploma, Agriculture, Management (BBA), and Nursing (B.Sc Nursing) on our Courses page.",
        }
        for key, reply in replies.items():
            if key in msg:
                return jsonify({"reply": reply, "mode": "faq"})
        return jsonify({
            "reply": "I can help with CUTM admissions, courses (B.Tech CSE, ECE, Mechanical, Civil, Diploma, Agriculture, BBA, B.Sc Nursing), fees, scholarships, and campus events. How can I assist you today?",
            "mode": "faq",
        })

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False)

