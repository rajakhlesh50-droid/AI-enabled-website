# 🏛️ CUTM AI-Enabled University Portal - Backend Documentation

This directory contains the complete backend application, relational persistence layer, AI predictive scoring engine, authentication services, and RESTful APIs powering **Centurion University of Technology and Management (CUTM)**'s digital portal.

---

## 🛠️ Technology Stack & Languages Used

| Layer / Component | Technology / Library | Role & Purpose |
| :--- | :--- | :--- |
| **Primary Language** | **Python (v3.12 / v3.14)** | High developer velocity, clean syntax, native data handling, and robust security libraries. |
| **Web Framework** | **Flask (v3.1.x)** | Lightweight, non-opinionated WSGI microframework providing fast routing, JSON serialization, and static dispatching. |
| **Cross-Origin Guard** | **Flask-CORS (v4.x)** | Manages Cross-Origin Resource Sharing headers for secure client-server communication. |
| **Database Engine** | **SQLite 3 (`data/university.db`)** | Embedded, serverless, ACID-compliant relational SQL engine with parameterized query safety. |
| **Password Cryptography** | **Werkzeug Security** | Salted `scrypt` / `PBKDF2` cryptographic password hashing (`generate_password_hash`, `check_password_hash`). |
| **Authorization Tokens** | **PyJWT (v2.15.x)** | Digitally signed, stateless JSON Web Tokens (`HS256`) with 24-hour expiration for sessions. |
| **Environment Loader** | **python-dotenv** | Loads development configurations securely from `.env` without hardcoding credentials. |
| **AI Predictive Engine** | **Algorithmic Evaluation Engine** | Calculates real-time admission chances and Chancellor Merit Scholarship tiers (up to 100% tuition waiver). |
| **AI Chatbot Service** | **Heuristic & LLM Proxy** | Instant 24/7 student guidance covering all 8 departments, admissions, fees, and campus events. |

---

## 📂 Backend File Architecture

```text
backend/
├── __init__.py           # Package marker for modular imports
├── app.py                # Main Flask WSGI application entry point and HTTP route handlers
├── config.py             # System configuration, paths, course catalog & sample event definitions
├── database.py           # SQLite connection pool, schema initialization, and transactional CRUD helpers
├── auth.py               # Cryptographic password hashing, JWT signing, verification and route guards
├── scoring.py            # AI composite lead scoring and admission prediction algorithms
├── ai_service.py         # Institutional FAQ knowledge-base and external LLM conversational service
├── models.py             # Domain data structures (User, Lead, Event, EventRegistration, Course)
├── requirements.txt      # Pinned Python package dependencies for the backend
├── .env.example          # Sample environment variables configuration template
├── README.md             # This comprehensive technical guide
└── data/
    └── university.db     # SQLite relational database file
```

---

## 📋 Relational Database Schema (`university.db`)

### 1. `users` Table
Manages accounts for students, applicants, and administrators:
- `id`: `INTEGER PRIMARY KEY AUTOINCREMENT`
- `username`: `TEXT UNIQUE NOT NULL`
- `email`: `TEXT UNIQUE NOT NULL`
- `phone`: `TEXT NULLABLE`
- `name`: `TEXT NOT NULL`
- `password_hash`: `TEXT NOT NULL` (Salted hash)
- `role`: `TEXT NOT NULL DEFAULT 'student'` (`student` or `admin`)
- `created_at`: `TEXT NOT NULL` (ISO 8601 UTC timestamp)

### 2. `leads` Table
Stores student admission applications:
- `id`: `INTEGER PRIMARY KEY AUTOINCREMENT`
- `data`: `TEXT NOT NULL` (JSON document storing `ref_id`, `name`, `email`, `phone`, `course`, `department`, `marks`, `city`, `state`, `message`, `score`, `status`, `created_at`)

### 3. `events` Table
Stores campus conferences, workshops, and seminars:
- `id`: `TEXT PRIMARY KEY` (UUID or slug)
- `data`: `TEXT NOT NULL` (JSON document storing `id`, `type`, `date`, `title`, `description`, `place`, `format`, `image`)

### 4. `event_registrations` Table
Stores student and attendee event registrations:
- `id`: `TEXT PRIMARY KEY` (UUID)
- `data`: `TEXT NOT NULL` (JSON document storing `id`, `name`, `email`, `phone`, `event_id`, `event_title`, `created_at`)

### 5. `app_settings` Table
Key-value persistent metadata (e.g., seeding flags):
- `key`: `TEXT PRIMARY KEY`
- `value`: `TEXT NOT NULL`

---

## 🌐 Complete REST API Endpoint Matrix

| Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Public | Serves the main university home page (`index.html`). |
| `GET` | `/admissions` | Public | Serves the Online Admissions & Merit Predictor portal (`admissions.html`). |
| `GET` | `/courses` | Public | Serves the Multi-Faculty Course Directory (`courses.html`). |
| `GET` | `/dashboard` | Public / Admin | Serves the Real-Time Counselor Administrative Console (`dashboard.html`). |
| `GET` | `/login` | Public | Serves the Dual-Tab Sign In & Registration portal (`login.html`). |
| `GET` | `/contact` | Public | Serves the Campus Contact & Location page (`contact.html`). |
| `GET` | `/gallery` | Public | Serves the Campus Visual Tour & Photo Gallery (`gallery.html`). |
| `GET` | `/overview` | Public | Serves the Institutional Overview & Accreditation credentials (`overview.html`). |
| `POST` | `/register` | Public | Creates a new student/admin account, generates salted hash, issues 24h JWT. |
| `POST` | `/login` | Public | Authenticates credentials, validates password against hash, issues JWT. |
| `GET` | `/api/me` | Bearer JWT | Returns current authenticated user profile (`id`, `username`, `name`, `role`). |
| `POST` | `/lead` | Public | Submits admission application, assigns `CUTM-XXXXXX` tracking ID, scores lead. |
| `GET` | `/leads` | Admin JWT | Retrieves all admission inquiries with scores and statuses. |
| `GET` | `/api/application-status/<query>` | Public | Searches admission status by Reference ID (`CUTM-XXXXXX`) or Mobile Number. |
| `POST` | `/predict` | Public | Evaluates board percentage against CUTM cutoffs for admission and scholarship tier. |
| `GET` | `/api/courses` | Public | Returns complete 8-program academic course catalog with seats and fees. |
| `PUT` | `/update/<phone>` | Admin JWT | Updates applicant status (`New`, `Contacted`, `Verified`, `Confirmed`, `Rejected`). |
| `DELETE` | `/delete/<phone>` | Admin JWT | Deletes an applicant record by phone number. |
| `GET` | `/stats` | Admin JWT | Returns statistical summary of leads grouped by academic department. |
| `GET` | `/events` | Public | Lists upcoming university conferences, workshops, and seminars. |
| `POST` | `/events` | Admin JWT | Creates a new academic campus event. |
| `PUT` | `/events/<id>` | Admin JWT | Updates an existing campus event. |
| `DELETE` | `/events/<id>` | Admin JWT | Deletes a campus event. |
| `GET` | `/registrations` | Admin JWT | Retrieves list of event attendee registrations. |
| `POST` | `/registrations` | Public | Registers a student for a specific campus event. |
| `DELETE` | `/registrations/<id>` | Admin JWT | Cancels/deletes an event registration. |
| `POST` | `/chat` | Public | Institutional 24/7 AI chatbot assistant with FAQ heuristic & LLM fallback. |

---

## 🚀 How to Run the Backend

### Option A: Using the Project Startup Script (Recommended)
From the workspace root directory:
```powershell
.\run.bat
```

### Option B: Running the Backend Directly via Python
```powershell
# 1. Activate the virtual environment
.\.venv\Scripts\activate

# 2. Navigate to the backend directory
cd backend

# 3. Start the Flask server
python app.py
```

The server will initialize the SQLite database automatically and serve on:
`http://127.0.0.1:5000/`

