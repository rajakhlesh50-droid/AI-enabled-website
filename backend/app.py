import datetime
import json
import os
import random
import sqlite3
import secrets
import urllib.error
import urllib.request
import uuid

import jwt
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
DATABASE_PATH = os.environ.get(
    "SQLITE_DB_PATH",
    os.path.join(BASE_DIR, "data", "university.db"),
)
if not os.path.isabs(DATABASE_PATH):
    DATABASE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", DATABASE_PATH))
os.makedirs(os.path.dirname(os.path.abspath(DATABASE_PATH)), exist_ok=True)

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

SECRET = os.environ.get("JWT_SECRET") or secrets.token_urlsafe(32)

DEFAULT_EVENTS = [
    {
        "id": "event-ai-conference",
        "type": "Conference",
        "date": "2026-10-24",
        "title": "Future of Responsible Artificial Intelligence & Engineering",
        "description": "A cross-disciplinary conversation at CUTM on building useful, trustworthy and human-centred AI and automation systems.",
        "place": "CUTM Main Auditorium",
        "format": "In person",
        "image": "images/cutm_photo_3.webp",
    },
    {
        "id": "event-analytics-workshop",
        "type": "Workshop",
        "date": "2026-11-05",
        "title": "From Data to Insight: Hands-on Tech Lab",
        "description": "Explore practical data analysis and engineering simulation techniques through guided exercises in CUTM labs.",
        "place": "CUTM Innovation Studio",
        "format": "Limited seats",
        "image": "images/cutm_photo_1.webp",
    },
    {
        "id": "event-sustainable-seminar",
        "type": "Seminar",
        "date": "2026-11-12",
        "title": "Sustainable Agriculture & Green Technology for Tomorrow",
        "description": "CUTM agricultural scientists and practitioners share ideas for precision farming and resilient rural communities.",
        "place": "CUTM Seminar Hall 2",
        "format": "Hybrid",
        "image": "images/cutm_photo_5.webp",
    },
    {
        "id": "event-design-workshop",
        "type": "Workshop",
        "date": "2026-11-19",
        "title": "Robotics & CAD/CAM Design Thinking Workshop",
        "description": "Hands-on mechanical prototyping and CAD modeling in the CUTM advanced fabrication workshop.",
        "place": "Learning Lab",
        "format": "Limited seats",
        "image": "images/cutm_photo_4.webp",
    },
    {
        "id": "event-research-conference",
        "type": "Conference",
        "date": "2026-12-03",
        "title": "National Conference on Healthcare, Nursing & Technology",
        "description": "A platform for emerging clinical research, nursing ethics, and smart healthcare technology at CUTM.",
        "place": "Convention Centre",
        "format": "In person",
        "image": "images/cutm_photo_8.webp",
    },
    {
        "id": "event-careers-seminar",
        "type": "Seminar",
        "date": "2026-12-10",
        "title": "Building Careers in Engineering & Business Management",
        "description": "Get industry perspectives on placements, campus hiring trends, and startup incubation pathways.",
        "place": "Online",
        "format": "Online",
        "image": "images/cutm_photo_6.webp",
    },
]

DEFAULT_COURSES = [
    {
        "id": "btech-cse",
        "name": "B.Tech Computer Science & Engineering (CSE)",
        "department": "Engineering & Technology",
        "short_code": "B.Tech CSE",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "10+2 with PCM (Min. 50% aggregate)",
        "description": "Comprehensive program in AI, Machine Learning, Cloud Computing, Cyber Security, Full-Stack Web Development, and Data Science.",
        "highlights": ["AI & Machine Learning Specialization", "Cloud Computing & DevOps Lab", "100% Placement Assistance with top MNCs"],
        "tag": "High Demand",
        "seats": 120,
        "fee": "₹1,10,000 / Year",
        "icon": "💻"
    },
    {
        "id": "btech-ece",
        "name": "B.Tech Electronics & Communication Engineering (ECE)",
        "department": "Engineering & Technology",
        "short_code": "B.Tech ECE",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "10+2 with PCM (Min. 50% aggregate)",
        "description": "Cutting-edge curriculum in VLSI design, Embedded Systems, IoT, Robotics, Signal Processing, and next-generation 5G telecommunication networks.",
        "highlights": ["Advanced VLSI & Embedded Systems Lab", "Robotics & IoT Prototyping", "Core Electronics & Telecom Placements"],
        "tag": "Future Ready",
        "seats": 60,
        "fee": "₹95,000 / Year",
        "icon": "📡"
    },
    {
        "id": "btech-mechanical",
        "name": "B.Tech Mechanical Engineering",
        "department": "Engineering & Technology",
        "short_code": "B.Tech Mechanical",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "10+2 with PCM (Min. 50% aggregate)",
        "description": "Practical training in CAD/CAM/CAE design, Robotics, Electric Vehicle (EV) technology, Thermodynamics, and Advanced Manufacturing.",
        "highlights": ["EV Technology & Robotics Labs", "Hands-on CNC Machining & 3D Printing", "Automotive & Aerospace Industry Ties"],
        "tag": "Industry 4.0",
        "seats": 60,
        "fee": "₹90,000 / Year",
        "icon": "⚙️"
    },
    {
        "id": "btech-civil",
        "name": "B.Tech Civil Engineering",
        "department": "Engineering & Technology",
        "short_code": "B.Tech Civil",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "10+2 with PCM (Min. 50% aggregate)",
        "description": "Modern infrastructure planning, Structural Analysis, Smart Cities development, Green Building architecture, and Geotechnical Surveying.",
        "highlights": ["Total Station & GIS Surveying", "Structural Design & Concrete Technology Labs", "Infrastructure & Government Project Internships"],
        "tag": "Core Engineering",
        "seats": 60,
        "fee": "₹85,000 / Year",
        "icon": "🏗️"
    },
    {
        "id": "diploma-engg",
        "name": "Diploma in Engineering (Polytechnic)",
        "department": "Polytechnic & Diploma Studies",
        "short_code": "Diploma",
        "duration": "3 Years (2 Years Lateral Entry)",
        "eligibility": "10th pass (Min. 45%) or 10+2 Science / ITI for Lateral Entry",
        "description": "Skill-oriented technical education offering specializations in Mechanical, Civil, Electrical, and CSE with heavy workshop practice.",
        "highlights": ["Practical Hands-on Workshop Training", "Direct Lateral Entry to B.Tech 2nd Year", "Junior Engineer & Technical Supervisor Roles"],
        "tag": "Skill Oriented",
        "seats": 120,
        "fee": "₹45,000 / Year",
        "icon": "🔧"
    },
    {
        "id": "bsc-agriculture",
        "name": "B.Sc. (Hons.) Agriculture",
        "department": "Agricultural Sciences",
        "short_code": "Agriculture",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "10+2 with PCB / PCM / Agriculture (Min. 50% aggregate)",
        "description": "Scientific training in modern Agronomy, Soil Sciences, Precision Hydroponics, Plant Breeding, Horticulture, and Sustainable Agri-Business.",
        "highlights": ["Dedicated Research Farms & Polyhouses", "Organic Farming & Soil Testing Laboratories", "Agri-Tech Startup Incubation & Extension Work"],
        "tag": "Research & Tech",
        "seats": 60,
        "fee": "₹80,000 / Year",
        "icon": "🌾"
    },
    {
        "id": "bba",
        "name": "BBA (Bachelor of Business Administration)",
        "department": "Management & Business Studies",
        "short_code": "BBA",
        "duration": "3 Years (6 Semesters)",
        "eligibility": "10+2 in any stream (Min. 45% aggregate)",
        "description": "Foundations of modern business management, financial analytics, marketing strategy, HR management, and startup entrepreneurship with live corporate projects.",
        "highlights": ["Case Study Pedagogy & Harvard Business Modules", "Corporate Mentorship & Paid Internships", "FinTech, Digital Marketing & Analytics Tracks"],
        "tag": "Leadership",
        "seats": 90,
        "fee": "₹65,000 / Year",
        "icon": "📊"
    },
    {
        "id": "bsc-nursing",
        "name": "B.Sc. Nursing",
        "department": "Nursing & Healthcare Sciences",
        "short_code": "B.Sc Nursing",
        "duration": "4 Years (INC Approved)",
        "eligibility": "10+2 with PCB & English (Min. 45-50% aggregate, Age 17+)",
        "description": "Professional nursing education combining intensive clinical rotations at multi-speciality partner hospitals, simulation training, and patient care ethics.",
        "highlights": ["Clinical Rotations in 500+ Bed Hospitals", "Advanced Simulation & Critical Care Labs", "Global & Domestic Healthcare Placements"],
        "tag": "Healthcare Career",
        "seats": 60,
        "fee": "₹1,05,000 / Year",
        "icon": "🩺"
    }
]


def request_data():
    return request.get_json(silent=True) or {}


def current_user():
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        return None
    try:
        payload = jwt.decode(authorization[7:], SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
    return payload


def admin_user():
    payload = current_user()
    if not payload:
        return None
    if payload.get("user") == "admin" or payload.get("role") == "admin":
        return "admin"
    return None


def require_admin():
    if admin_user() != "admin":
        return jsonify({"error": "Admin authentication required."}), 401
    return None


def get_db():
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db():
    with get_db() as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, data TEXT NOT NULL)"
        )
        connection.execute(
            "CREATE TABLE IF NOT EXISTS event_registrations (id TEXT PRIMARY KEY, data TEXT NOT NULL)"
        )
        connection.execute(
            "CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL)"
        )
        connection.execute(
            "CREATE TABLE IF NOT EXISTS app_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'student',
                created_at TEXT NOT NULL
            )"""
        )
        admin_check = connection.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()
        if not admin_check:
            connection.execute(
                "INSERT INTO users (username, email, phone, name, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    "admin",
                    "admin@cutm.ac.in",
                    "1800123456",
                    "CUTM Administrator",
                    generate_password_hash("admin1234"),
                    "admin",
                    datetime.datetime.now(datetime.timezone.utc).isoformat()
                )
            )
        seeded = connection.execute(
            "SELECT value FROM app_settings WHERE key = 'sample_events_seeded'"
        ).fetchone()
        if not seeded:
            connection.executemany(
                "INSERT OR IGNORE INTO events (id, data) VALUES (?, ?)",
                [(event["id"], json.dumps(event)) for event in DEFAULT_EVENTS],
            )
            connection.execute(
                "INSERT INTO app_settings (key, value) VALUES ('sample_events_seeded', 'true')"
            )


def list_event_documents():
    with get_db() as connection:
        rows = connection.execute("SELECT data FROM events").fetchall()
    event_documents = [json.loads(row["data"]) for row in rows]
    return sorted(event_documents, key=lambda event: event["date"])


def find_event(event_id):
    with get_db() as connection:
        row = connection.execute(
            "SELECT data FROM events WHERE id = ?", (event_id,)
        ).fetchone()
    return json.loads(row["data"]) if row else None


def replace_event(event):
    with get_db() as connection:
        connection.execute(
            "INSERT INTO events (id, data) VALUES (?, ?) "
            "ON CONFLICT(id) DO UPDATE SET data = excluded.data",
            (event["id"], json.dumps(event)),
        )


def list_registration_documents():
    with get_db() as connection:
        rows = connection.execute(
            "SELECT data FROM event_registrations ORDER BY rowid DESC"
        ).fetchall()
    return [json.loads(row["data"]) for row in rows]


def list_lead_documents():
    with get_db() as connection:
        rows = connection.execute("SELECT data FROM leads ORDER BY id DESC").fetchall()
    return [json.loads(row["data"]) for row in rows]


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


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request_data()
    message = data.get("message", "")
    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Please provide a message."}), 400
    message = message.strip()
    if len(message) > 2000:
        return jsonify({"error": "Messages must be 2,000 characters or fewer."}), 400

    api_key = os.environ.get("AI_API_KEY")
    if api_key:
        endpoint = os.environ.get("AI_API_URL", "https://api.openai.com/v1/chat/completions")
        model = os.environ.get("AI_MODEL", "gpt-4o-mini")
        event_context = "\n".join(
            f"- {event['title']} ({event['type']}, {event['date']}, {event['format']}, {event['place']}): {event['description']}"
            for event in list_event_documents()
        )
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are the CUTM (Centurion University of Technology and Management) assistant. "
                        "Answer helpfully and concisely about CUTM admissions, courses (B.Tech CSE, ECE, Mechanical, Civil, "
                        "Diploma, Agriculture, BBA, B.Sc Nursing), fees, scholarships, and campus events. "
                        "Direct visitors to admissions@cutm.ac.in for official admission guidance.\n\n"
                        f"Current events:\n{event_context}"
                    ),
                },
                {"role": "user", "content": message},
            ],
            "temperature": 0.4,
        }
        request_object = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request_object, timeout=20) as response:
                result = json.loads(response.read().decode("utf-8"))
            reply = result["choices"][0]["message"]["content"]
            if not isinstance(reply, str) or not reply.strip():
                raise ValueError("AI provider returned an empty reply.")
            return jsonify({"reply": reply.strip(), "mode": "ai"})
        except urllib.error.HTTPError as error:
            return jsonify({"error": f"AI provider returned HTTP {error.code}."}), 502
        except (urllib.error.URLError, TimeoutError, KeyError, IndexError, ValueError, json.JSONDecodeError) as error:
            return jsonify({"error": f"AI assistant is unavailable: {error}"}), 502

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
        "admission": "Admissions 2026-2027 are OPEN for B.Tech (CSE, ECE, Mechanical, Civil), Diploma, Agriculture, BBA, and B.Sc Nursing. Apply online on our Admissions page or call 1800-123-4567.",
        "apply": "You can apply online right now! Head to the Admissions page, choose your department and course, and submit your application with instant eligibility check.",
        "fee": "Annual fees: B.Tech CSE: ₹1,10,000 | B.Tech ECE: ₹95,000 | Mechanical: ₹90,000 | Civil: ₹85,000 | Diploma: ₹45,000 | Agriculture: ₹80,000 | BBA: ₹65,000 | B.Sc Nursing: ₹1,05,000.",
        "fees": "Annual fees: B.Tech CSE: ₹1,10,000 | B.Tech ECE: ₹95,000 | Mechanical: ₹90,000 | Civil: ₹85,000 | Diploma: ₹45,000 | Agriculture: ₹80,000 | BBA: ₹65,000 | B.Sc Nursing: ₹1,05,000.",
        "scholarship": "We offer Chancellor Merit Scholarships: up to 100% tuition waiver for 90%+ marks, and 25%-50% for 75-89% marks, plus sports and defense quotas.",
        "eligibility": "Eligibility: B.Tech requires 10+2 PCM (50%); B.Sc Nursing requires 10+2 PCB (45-50%); B.Sc Agriculture requires 10+2 PCB/PCM (50%); BBA requires 10+2 (45%); Diploma requires 10th (45%).",
        "register": "Select Register on an event card to submit your details and reserve your place.",
        "registration": "Select Register on an event card to submit your details and reserve your place.",
        "contact": "You can reach our admissions and university team at admissions@aiuniversity.edu or events@aiuniversity.edu.",
        "course": "Explore our departments: Engineering (B.Tech CSE, ECE, Mech, Civil), Diploma, Agriculture, Management (BBA), and Nursing (B.Sc Nursing) on our Courses page.",
        "event": "Explore the upcoming conferences, workshops and seminars in the Events section. You can filter by program type or search by topic.",
        "conference": "Our conferences bring people together to share research and ideas across disciplines. Check the Events section for upcoming programs.",
        "workshop": "Workshops offer practical, hands-on learning. Browse the Events section for upcoming topics, dates and formats.",
        "seminar": "Seminars feature focused talks and conversations with experts. Upcoming programs are listed in the Events section.",
    }
    for key, reply in replies.items():
        if key in msg:
            return jsonify({"reply": reply, "mode": "faq"})
    return jsonify(
        {
            "reply": "I can help with admissions, courses (B.Tech CSE, ECE, Mechanical, Civil, Diploma, Agriculture, BBA, B.Sc Nursing), and events. How can I assist you today?",
            "mode": "faq",
        }
    )


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

    token = jwt.encode(
        {
            "user": username,
            "user_id": user_id,
            "role": role,
            "name": name,
            "email": email,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        },
        SECRET,
        algorithm="HS256"
    )

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

    # 1. Check database users table
    with get_db() as connection:
        user_row = connection.execute(
            "SELECT * FROM users WHERE lower(username) = ? OR lower(email) = ?", (login_id, login_id)
        ).fetchone()

    if user_row:
        if check_password_hash(user_row["password_hash"], password):
            token = jwt.encode(
                {
                    "user": user_row["username"],
                    "user_id": user_row["id"],
                    "role": user_row["role"],
                    "name": user_row["name"],
                    "email": user_row["email"],
                    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
                },
                SECRET,
                algorithm="HS256"
            )
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

    # 2. Fallback check for environment admin credentials
    admin_username = os.environ.get("ADMIN_USERNAME", "admin").lower()
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin1234")
    if login_id == admin_username and password == admin_password:
        token = jwt.encode(
            {
                "user": "admin",
                "role": "admin",
                "name": "CUTM Administrator",
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
            },
            SECRET,
            algorithm="HS256"
        )
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


def score(data):
    total = 0
    course = str(data.get("course", "")).lower()
    if any(k in course for k in ["b.tech", "cse", "ece", "mechanical", "civil", "engineering"]):
        total += 50
    elif "nursing" in course:
        total += 45
    elif "agriculture" in course:
        total += 45
    elif "bba" in course:
        total += 40
    elif "diploma" in course:
        total += 35
    else:
        total += 30

    phone = "".join(character for character in str(data.get("phone", "")) if character.isdigit())
    if len(phone) == 10:
        total += 25

    try:
        marks = float(data.get("marks", 0))
        if marks >= 80:
            total += 25
        elif marks >= 60:
            total += 15
        elif marks >= 45:
            total += 10
    except (TypeError, ValueError):
        pass

    return total


@app.route("/api/courses", methods=["GET"])
def get_courses_api():
    return jsonify(DEFAULT_COURSES)


@app.route("/admissions")
def admissions_view():
    return send_from_directory(FRONTEND_DIR, "admissions.html")


@app.route("/courses")
def courses_view():
    return send_from_directory(FRONTEND_DIR, "courses.html")


@app.route("/dashboard")
def dashboard_view():
    return send_from_directory(FRONTEND_DIR, "dashboard.html")


@app.route("/contact")
def contact_view():
    return send_from_directory(FRONTEND_DIR, "contact.html")


@app.route("/gallery")
def gallery_view():
    return send_from_directory(FRONTEND_DIR, "gallery.html")


@app.route("/overview")
def overview_view():
    return send_from_directory(FRONTEND_DIR, "overview.html")


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
    return jsonify(
        {
            "total": len(lead_documents),
            "courses": [{"_id": course, "count": count} for course, count in course_totals.items()],
        }
    )


@app.route("/predict", methods=["POST"])
def predict():
    data = request_data()
    try:
        marks = float(data.get("marks", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Marks must be a number."}), 400

    course = data.get("course", "General")
    if marks >= 80:
        prediction = "High"
        scholarship = "Eligible for 50% - 100% Merit Scholarship"
        message = "Outstanding score! Very high chance of direct admission in 1st Merit List."
    elif marks >= 60:
        prediction = "High"
        scholarship = "Eligible for 25% Merit Scholarship"
        message = "Great score! High chance of admission in your selected course."
    elif marks >= 45:
        prediction = "Moderate"
        scholarship = "Standard Merit Seat"
        message = "Eligible for counseling round and seat confirmation."
    else:
        prediction = "Low"
        scholarship = "Counseling Recommended"
        message = "Marks below minimum criteria (45%). Please contact admission counselor."

    return jsonify({
        "prediction": prediction,
        "marks": marks,
        "course": course,
        "scholarship": scholarship,
        "message": message
    })


initialize_db()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
