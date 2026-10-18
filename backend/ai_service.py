"""
Centurion University of Technology and Management (CUTM)
Backend AI Service - 24/7 Chatbot & Admissions Knowledge Assistant
"""

import json
import urllib.error
import urllib.request

try:
    from .config import AI_API_KEY, AI_API_URL, AI_MODEL
except ImportError:
    from config import AI_API_KEY, AI_API_URL, AI_MODEL

# Knowledge Base & Institutional Heuristic Replies
FAQ_KNOWLEDGE_BASE = {
    "cse": "B.Tech Computer Science & Engineering (CSE) offers advanced training in AI, Machine Learning, Cloud Computing, Cyber Security, and Web Technologies with high placement rates.",
    "computer": "B.Tech CSE covers Artificial Intelligence, Data Science, Cloud Systems, and Full-Stack Development. Check the Courses or Admissions page to apply.",
    "ece": "B.Tech Electronics & Communication Engineering (ECE) specializes in VLSI Design, Embedded Systems, IoT, Robotics, and 5G Communications.",
    "mechanical": "B.Tech Mechanical Engineering focuses on Robotics, CAD/CAM/CAE, EV Technology, Automation, and Advanced Manufacturing with modern lab infrastructure.",
    "machnical": "B.Tech Mechanical Engineering focuses on Robotics, CAD/CAM/CAE, EV Technology, Automation, and Advanced Manufacturing with modern lab infrastructure.",
    "civil": "B.Tech Civil Engineering covers Smart Cities, Structural Analysis, Green Building Design, Total Station Surveying, and Infrastructure Engineering.",
    "b.tech": "We offer B.Tech degrees in 4 high-demand engineering branches: CSE, ECE, Mechanical, and Civil Engineering (4 Years duration, 10+2 PCM with min 50%).",
    "btech": "We offer B.Tech degrees in 4 high-demand engineering branches: CSE, ECE, Mechanical, and Civil Engineering (4 Years duration, 10+2 PCM with min 50%).",
    "engineering": "Our Engineering faculty offers B.Tech in CSE, ECE, Mechanical, and Civil, as well as Diploma in Engineering (Polytechnic).",
    "diploma": "Diploma (Polytechnic) is a 3-year practical program (2-year lateral entry) in CSE, Mechanical, Civil, and Electrical for 10th or 12th/ITI students.",
    "polytechnic": "Diploma (Polytechnic) is a 3-year career-focused engineering program after 10th or 10+2/ITI with hands-on workshop training.",
    "agriculture": "B.Sc. (Hons.) Agriculture is a 4-year degree covering Agronomy, Precision Farming, Soil Science, Horticulture, and Agri-Business on dedicated research farms.",
    "agriculure": "B.Sc. (Hons.) Agriculture is a 4-year degree covering Agronomy, Precision Farming, Soil Science, Horticulture, and Agri-Business on dedicated research farms.",
    "bba": "BBA (Bachelor of Business Administration) is a 3-year undergraduate program focusing on Marketing, Finance, HR, Entrepreneurship, and Business Analytics.",
    "nursing": "B.Sc. Nursing is an INC-approved 4-year healthcare program with clinical hospital rotations, simulation labs, and global career opportunities.",
    "admission": "Admissions 2026-2027 are OPEN for B.Tech (CSE, ECE, Mechanical, Civil), Diploma, Agriculture, BBA, and B.Sc Nursing. Apply online on our Admissions page or call 1800-123-4567.",
    "apply": "You can apply online right now! Head to the Admissions page, choose your department and course, and submit your application with instant eligibility check.",
    "fee": "Annual fees: B.Tech CSE: ₹1,10,000 | B.Tech ECE: ₹95,000 | Mechanical: ₹90,000 | Civil: ₹85,000 | Diploma: ₹45,000 | Agriculture: ₹80,000 | BBA: ₹65,000 | B.Sc Nursing: ₹1,05,000.",
    "fees": "Annual fees: B.Tech CSE: ₹1,10,000 | B.Tech ECE: ₹95,000 | Mechanical: ₹90,000 | Civil: ₹85,000 | Diploma: ₹45,000 | Agriculture: ₹80,000 | BBA: ₹65,000 | B.Sc Nursing: ₹1,05,000.",
    "scholarship": "We offer Chancellor Merit Scholarships: up to 100% tuition waiver for 90%+ marks, and 25%-50% for 75-89% marks, plus sports and defense quotas.",
    "eligibility": "Eligibility: B.Tech requires 10+2 PCM (50%); B.Sc Nursing requires 10+2 PCB (45-50%); B.Sc Agriculture requires 10+2 PCB/PCM (50%); BBA requires 10+2 (45%); Diploma requires 10th (45%).",
    "register": "Select Register on an event card to submit your details and reserve your place.",
    "registration": "Select Register on an event card to submit your details and reserve your place.",
    "contact": "You can reach our admissions and university team at admissions@cutm.ac.in or call 1800-123-4567.",
    "course": "Explore our departments: Engineering (B.Tech CSE, ECE, Mech, Civil), Diploma, Agriculture, Management (BBA), and Nursing (B.Sc Nursing) on our Courses page.",
    "event": "Explore upcoming conferences, workshops and seminars in the Events section. You can filter by program type or search by topic.",
    "conference": "Our conferences bring people together to share research and ideas across disciplines. Check the Events section for upcoming programs.",
    "workshop": "Workshops offer practical, hands-on learning. Browse the Events section for upcoming topics, dates and formats.",
    "seminar": "Seminars feature focused talks and conversations with experts. Upcoming programs are listed in the Events section.",
}


def generate_chat_reply(message: str, events_list: list = None) -> dict:
    """
    Generates an intelligent reply to student questions.
    Uses external LLM (OpenAI/Gemini/etc.) if AI_API_KEY is present,
    otherwise uses the built-in fast institutional FAQ heuristic engine.
    """
    if not isinstance(message, str) or not message.strip():
        return {"error": "Please provide a valid message.", "status": 400}

    clean_message = message.strip()
    if len(clean_message) > 2000:
        return {"error": "Messages must be 2,000 characters or fewer.", "status": 400}

    # 1. External LLM Path (if API key configured)
    if AI_API_KEY:
        event_context = ""
        if events_list:
            event_context = "\n".join(
                f"- {e.get('title')} ({e.get('type')}, {e.get('date')}, {e.get('format')}, {e.get('place')}): {e.get('description')}"
                for e in events_list
            )

        payload = {
            "model": AI_MODEL,
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
                {"role": "user", "content": clean_message},
            ],
            "temperature": 0.4,
        }

        request_object = urllib.request.Request(
            AI_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {AI_API_KEY}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request_object, timeout=20) as response:
                result = json.loads(response.read().decode("utf-8"))
            reply = result["choices"][0]["message"]["content"]
            if reply and reply.strip():
                return {"reply": reply.strip(), "mode": "ai", "status": 200}
        except Exception:
            pass  # Fall through to FAQ on network or auth errors

    # 2. Institutional Heuristic Matching
    lower_msg = clean_message.lower()
    for keyword, response in FAQ_KNOWLEDGE_BASE.items():
        if keyword in lower_msg:
            return {"reply": response, "mode": "faq", "status": 200}

    # Default institutional fallback
    return {
        "reply": "I can help with CUTM admissions, courses (B.Tech CSE, ECE, Mechanical, Civil, Diploma, Agriculture, BBA, B.Sc Nursing), fees, and scholarships. How can I assist you today?",
        "mode": "faq",
        "status": 200
    }

