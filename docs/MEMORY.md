# System Memory, State & Architectural Decisions
## Centurion University of Technology and Management (CUTM)

---

### 1. Active Environment & Configuration Memory

- **Operating System:** Windows (PowerShell Shell).
- **Backend Framework:** Python 3.14 + Flask 3.1.3 + Werkzeug 3.1.9 + PyJWT 2.15.1 + Flask-CORS.
- **Port & Host:** `http://127.0.0.1:5000` (Localhost Port 5000).
- **Virtual Environment Path:** `c:\Users\rajak\OneDrive\Desktop\AI-enabled website\.venv`.
- **Database Engine & Path:** SQLite 3 database located at `backend/data/university.db`.
- **Primary Static / Template Directory:** `frontend/` (actively served by Flask static routing), mirrored in `template/` (and `templates/`) and `static/` (and `statics/`).
- **Modular Core Directory:** `src/` (contains package factory, modular database, auth, and scoring services).

---

### 2. Default Administrative Credentials
- **Role:** Administrator (`admin`)
- **Username:** `admin` (or `admin@cutm.ac.in`)
- **Password:** `admin1234`
- **Dashboard URI:** `http://127.0.0.1:5000/dashboard.html`
- **Token Mechanism:** JWT Token stored in browser `localStorage` as `"token"` with 24-hour expiration.

---

### 3. Institutional Identity & Assets
- **University Full Name:** Centurion University of Technology and Management (CUTM).
- **Official Motto / Slogan:** *"ज्ञानस्य संयोगाय वितरणाय च"* | *"CONNECTING THROUGH KNOWLEDGE"*.
- **Sub-tagline:** *"Shaping lives, empowering communities."*
- **Helpline Phone:** `1800-123-CUTM` (or `1800-123-4567`).
- **Admissions Desk Email:** `admissions@cutm.ac.in`.
- **Brand Logo Asset:** `images/cutm_logo.png` (transparent high-resolution circular emblem).
- **Favicon:** Set to `images/cutm_logo.png` on all pages.

---

### 4. Key Architectural Decisions (ADRs)

#### ADR-001: Zero-Dependency Pure Frontend
- **Decision:** Keep frontend purely in semantic HTML5, CSS3, and ES6+ JavaScript rather than heavy client frameworks like React or Angular.
- **Rationale:** Ensures instant load times, zero build/compile step, simple one-click maintenance, and direct file editing capability.

#### ADR-002: Dual Path Structure (`frontend` + `template` / `static` + `src`)
- **Decision:** Maintain public pages in `frontend/` for direct Flask static serving, while keeping synchronized standards in `template/` (HTML), `static/` (CSS/Images/JS), and `src/` (Modular Python).
- **Rationale:** Satisfies both the existing fast development workflow and standard Python/Flask enterprise architectural conventions.

#### ADR-003: Salted Password Hashing & Flexible Login ID
- **Decision:** Use `werkzeug.security` with PBKDF2/scrypt salting for user registration in SQLite, while allowing users to sign in using either their `username` OR their `email`.
- **Rationale:** Enhances user experience while maintaining industry-standard cryptographic security.

#### ADR-004: Real-Time Admin Notification Engine
- **Decision:** Employ a dual-notification system:
  1. Server terminal formatted ASCII box logging.
  2. Client-side lightweight polling (10s interval) in `dashboard.html` that triggers Web Audio chime and floating toast banner when a new lead is detected.
- **Rationale:** Eliminates the complexity and server overhead of WebSockets while providing immediate, reliable awareness to admissions counselors.

#### ADR-005: Official Reference ID Format (`CUTM-XXXXXX`)
- **Decision:** Generate official reference codes on the server in format `CUTM-` followed by a random 6-digit integer (`100000` to `999999`).
- **Rationale:** Provides students with a memorable identifier for phone counseling and status tracking.

