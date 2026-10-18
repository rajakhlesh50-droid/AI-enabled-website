"""
Centurion University of Technology and Management (CUTM)
Backend Configuration Module
"""

import os
import secrets
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "templates"))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "static"))

# Database Configuration
DATABASE_PATH = os.environ.get(
    "SQLITE_DB_PATH",
    os.path.join(BASE_DIR, "data", "university.db"),
)
if not os.path.isabs(DATABASE_PATH):
    DATABASE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", DATABASE_PATH))
os.makedirs(os.path.dirname(os.path.abspath(DATABASE_PATH)), exist_ok=True)

# Security and Authentication
SECRET = os.environ.get("JWT_SECRET") or secrets.token_urlsafe(32)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin").lower()
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin1234")
PORT = int(os.environ.get("PORT", 5000))

# AI Provider Configuration
AI_API_KEY = os.environ.get("AI_API_KEY")
AI_API_URL = os.environ.get("AI_API_URL", "https://api.openai.com/v1/chat/completions")
AI_MODEL = os.environ.get("AI_MODEL", "gpt-4o-mini")

# Academic Departments & Course Catalog (8 High-Demand Programs)
DEFAULT_COURSES = [
    {
        "id": "btech-cse",
        "name": "B.Tech Computer Science & Engineering (CSE)",
        "department": "Engineering & Technology",
        "short_code": "B.Tech CSE",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "10+2 with PCM (Min. 50% aggregate)",
        "description": "Comprehensive program in AI, Machine Learning, Cloud Computing, Cyber Security, Full-Stack Web Development, and Data Science.",
        "highlights": [
            "AI & Machine Learning Specialization",
            "Cloud Computing & DevOps Lab",
            "100% Placement Assistance with top MNCs"
        ],
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
        "highlights": [
            "Advanced VLSI & Embedded Systems Lab",
            "Robotics & IoT Prototyping",
            "Core Electronics & Telecom Placements"
        ],
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
        "highlights": [
            "EV Technology & Robotics Labs",
            "Hands-on CNC Machining & 3D Printing",
            "Automotive & Aerospace Industry Ties"
        ],
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
        "highlights": [
            "Total Station & GIS Surveying",
            "Structural Design & Concrete Technology Labs",
            "Infrastructure & Government Project Internships"
        ],
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
        "highlights": [
            "Practical Hands-on Workshop Training",
            "Direct Lateral Entry to B.Tech 2nd Year",
            "Junior Engineer & Technical Supervisor Roles"
        ],
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
        "highlights": [
            "Dedicated Research Farms & Polyhouses",
            "Organic Farming & Soil Testing Laboratories",
            "Agri-Tech Startup Incubation & Extension Work"
        ],
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
        "highlights": [
            "Case Study Pedagogy & Harvard Business Modules",
            "Corporate Mentorship & Paid Internships",
            "FinTech, Digital Marketing & Analytics Tracks"
        ],
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
        "highlights": [
            "Clinical Rotations in 500+ Bed Hospitals",
            "Advanced Simulation & Critical Care Labs",
            "Global & Domestic Healthcare Placements"
        ],
        "tag": "Healthcare Career",
        "seats": 60,
        "fee": "₹1,05,000 / Year",
        "icon": "🩺"
    }
]

# Campus Events & Academic Programs
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

