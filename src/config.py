import os
import secrets
from dotenv import load_dotenv

load_dotenv()

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "templates")
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

DATABASE_PATH = os.environ.get(
    "SQLITE_DB_PATH",
    os.path.join(PROJECT_ROOT, "backend", "data", "university.db"),
)
if not os.path.isabs(DATABASE_PATH):
    DATABASE_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, DATABASE_PATH))
os.makedirs(os.path.dirname(os.path.abspath(DATABASE_PATH)), exist_ok=True)

SECRET = os.environ.get("JWT_SECRET") or secrets.token_urlsafe(32)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin1234")

DEFAULT_COURSES = [
    {
        "id": "btech-cse",
        "name": "B.Tech Computer Science & Engineering (CSE)",
        "department": "Engineering & Technology",
        "short_code": "CSE",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "10+2 with Physics, Mathematics & Chemistry/CS (Min. 50% aggregate)",
        "description": "Comprehensive program focusing on AI, Cloud Computing, Full-Stack Software Engineering, Data Science, Cyber Security, and IoT.",
        "highlights": ["Industry Co-Designed Curriculum with AWS & IBM", "100% Placement Assistance with High Package Roles", "State-of-the-art Supercomputing & AI Labs"],
        "tag": "Most Popular",
        "seats": 180,
        "fee": "₹1,10,000 / Year",
        "icon": "💻"
    },
    {
        "id": "btech-ece",
        "name": "B.Tech Electronics & Communication Engineering (ECE)",
        "department": "Engineering & Technology",
        "short_code": "ECE",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "10+2 with PCM (Min. 50% aggregate)",
        "description": "Cutting-edge curriculum in VLSI Design, Embedded Systems, 5G Communications, Robotics, and IoT sensor networks.",
        "highlights": ["Cadence & MATLAB Advanced EDA Design Labs", "Robotics & Drone Fabrication Workshops", "Recruitment by Qualcomm, Intel, Tata Elxsi & ISRO"],
        "tag": "High Growth",
        "seats": 120,
        "fee": "₹95,000 / Year",
        "icon": "📡"
    },
    {
        "id": "btech-mech",
        "name": "B.Tech Mechanical Engineering",
        "department": "Engineering & Technology",
        "short_code": "Mechanical",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "10+2 with PCM (Min. 50% aggregate)",
        "description": "Specializations in Electric Vehicles (EV), Mechatronics, Industrial Automation, CAD/CAM/CAE, and Sustainable Energy Systems.",
        "highlights": ["Automotive Center of Excellence with CNC Machining", "Hands-on Student Formula Racing & Baja Teams", "Placements in Tata Motors, L&T, Mahindra & Bosch"],
        "tag": "Industry 4.0",
        "seats": 90,
        "fee": "₹90,000 / Year",
        "icon": "⚙️"
    },
    {
        "id": "btech-civil",
        "name": "B.Tech Civil Engineering",
        "department": "Engineering & Technology",
        "short_code": "Civil",
        "duration": "4 Years (8 Semesters)",
        "eligibility": "10+2 with PCM (Min. 50% aggregate)",
        "description": "Hands-on engineering covering Smart City Infrastructure, GIS & Remote Sensing, Green Buildings, and Structural Simulation.",
        "highlights": ["Total Station & Advanced Geotechnical Labs", "Live Government Smart Infrastructure Projects", "Careers in NHAI, Larsen & Toubro, CPWD, Afcons"],
        "tag": "Infrastructure",
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
        "image": "images/cutm_photo_8.webp",
    },
]

