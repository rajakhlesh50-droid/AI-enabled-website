# Product Requirements Document (PRD)
## Centurion University of Technology and Management (CUTM) — AI-Enabled Web Portal

---

### 1. Executive Summary
The CUTM AI-Enabled Web Portal is an intelligent university website and admissions management platform designed for Centurion University of Technology and Management (CUTM). It delivers an engaging, responsive experience for prospective students, parents, faculty, and administrative staff. Key highlights include an AI-driven merit and scholarship predictor, automated admissions intake, real-time administrative applicant dashboard with live alerts, role-based registration/login, and an interactive campus events hub.

---

### 2. Goals & Objectives
- **Modern Institutional Presence:** Showcase CUTM's academic offerings, NAAC A+ accreditation, campus infrastructure, research farms, and high-placement records.
- **Streamlined Admissions Pipeline:** Enable direct online applications for 8 high-demand academic departments with instant reference code generation (`CUTM-XXXXXX`).
- **AI Merit & Scholarship Predictor:** Empower prospective students to estimate admission probability and scholarship eligibility in real time based on 10th/12th board marks.
- **Centralized Admin Lead Management:** Provide counselors with live table updates, search/filtering, CSV exports for Excel, and one-click WhatsApp/Call outreach.
- **Secure Dual-Role Authentication:** Support both Student and Faculty/Admin registration and JWT-based session security.

---

### 3. Target Audience & Personas
1. **Prospective Student:** Looks for course details, eligibility criteria, annual fees, scholarship waivers, and applies online.
2. **Parent / Guardian:** Reviews accreditation, campus safety, placement records, hostel facilities, and transport routes.
3. **Admissions Officer / Admin Counselor:** Monitors incoming leads in real time, changes lead verification status, downloads applicant spreadsheets, and initiates phone/WhatsApp counseling.
4. **Faculty / Staff:** Manages university conferences, workshops, seminars, and attendee registrations.

---

### 4. Core Features & Functional Requirements

#### 4.1 Academic Course Catalog
The platform maintains an authoritative catalog of programs across 5 faculties:
- **Engineering & Technology:** B.Tech Computer Science & Engineering (CSE), B.Tech Electronics & Communication (ECE), B.Tech Mechanical Engineering, B.Tech Civil Engineering.
- **Polytechnic Studies:** 3-Year Diploma in Engineering (Polytechnic) with lateral entry to B.Tech 2nd Year.
- **Agricultural Sciences:** 4-Year B.Sc. (Hons.) Agriculture with experiential research farms.
- **Management & Business Studies:** 3-Year BBA with FinTech, Digital Marketing, and Corporate Mentorship.
- **Healthcare & Nursing:** 4-Year INC-Approved B.Sc. Nursing with multi-specialty clinical hospital rotations.

#### 4.2 Online Admissions & Lead Intake
- Form collects: Full Name, Email, 10-Digit Mobile Number, 10th/12th Marks (%), Department, Course, City, State, and Student Remarks/Queries.
- Automatically generates official reference identifier: `CUTM-XXXXXX`.
- Computes AI Lead Score (0–100) combining course demand, contact completeness, and academic merit percentage.
- Notifies counselors via terminal alert block and real-time dashboard banner.

#### 4.3 AI Merit & Scholarship Predictor
- Takes candidate's marks percentage and target program.
- Evaluates against historical CUTM merit criteria:
  - `>= 80%`: High admission chance + 50%–100% Chancellor Merit Scholarship eligibility.
  - `60%–79%`: High admission chance + 25% Merit Scholarship.
  - `45%–59%`: Moderate chance (counseling round seat confirmation).
  - `< 45%`: Counseling recommended / eligibility review.

#### 4.4 Admin Dashboard & Counseling Hub
- Protected by JWT authentication (`/login`).
- Summary KPI Cards: Total Applications, Top In-Demand Department, Average Applicant Marks, Event Registrations.
- Live Auto-Polling (every 10s) with audio chime and toast notification on new submissions.
- Instant search and multi-criteria filters (Course, Status).
- One-click **Export to CSV (Excel)** download.
- Direct communication actions: 💬 WhatsApp Web chat (`https://wa.me/91...`), 📞 Direct Call (`tel:`), 👁️ Full Application Detail Modal.

#### 4.5 Dual-Tab Authentication (Login & Register)
- Tab 1: **Sign In** (Username or Email + Password).
- Tab 2: **Register** (Full Name, Username, Role selection, Email, Mobile, Password with confirmation check).
- Passwords safely hashed using `werkzeug.security`.

#### 4.6 Campus Events & Workshop Hub
- Dynamic event creation, modification, and deletion for Conferences, Workshops, and Seminars.
- Interactive student registration modal with email and phone validation.

#### 4.7 24/7 AI University Assistant
- Rule-based & LLM-compatible chatbot responding to admissions, branches, fees, scholarships, and campus facilities.

---

### 5. Non-Functional Requirements
- **Performance:** Sub-100ms response time for local API routes; lightweight zero-dependency frontend.
- **Security:** JWT authentication (HS256), salted password hashing, parameter validation, input escaping against XSS.
- **Responsiveness:** Fluid grid layout matching mobile, tablet, laptop, and ultra-wide desktop viewports.
- **Compatibility:** Works on all evergreen browsers (Chrome, Edge, Firefox, Safari) and standard Windows/Linux/macOS hosting.

