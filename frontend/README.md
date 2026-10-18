# 🎨 CUTM AI-Enabled University Portal - Frontend Documentation

This directory contains the user interface, pages, responsive layouts, client-side scripts, and visual design assets for **Centurion University of Technology and Management (CUTM)**.

---

## 🏛️ Frontend Pages & Features Overview

### 1. `index.html` - CUTM Official University Home Page
- **Restored Official Circular Emblem (`images/cutm_logo.png`)**:
  - Features the authentic Sanskrit motto *"ज्ञानस्य संयोगाय वितरणाय च"* ("Connecting Through Knowledge"), sacred peacock emblem, and radiant sun of enlightenment.
- **Scenic Panoramic Campus Hero (`images/cutm_campus_hero.jpg`)**:
  - High-definition wide-angle photography of CUTM's lush green hilltop campus, with responsive typography and direct action buttons.
- **Quick Admissions Inquiry Module**:
  - Immediate lead capture form routing applicant inquiries directly to university counselors.
- **8 Academic Department Cards**:
  - Highlights Engineering (CSE, ECE, Mech, Civil), Polytechnic, Agriculture, Management (BBA), and Healthcare (B.Sc. Nursing).
- **Accreditation & Highlights Showcase**:
  - Displays NAAC Grade 'A+', 150+ high-tech laboratories, 100% placement assistance, and 5 Odisha campuses.
- **24/7 AI University Assistant Widget**:
  - Interactive floating chat modal with instant heuristic and AI responses.

### 2. `admissions.html` - Online Admissions & AI Merit Evaluation Portal
- **Online Admission Application Pipeline**:
  - Captures applicant details, high-school/12th percentages, preferred course, and location.
  - Automatically generates an official reference tracking code: `CUTM-XXXXXX`.
- **Interactive AI Merit & Scholarship Predictor**:
  - Real-time client evaluator calculating admission probability and Chancellor Merit Scholarship tiers (up to 100% tuition waiver).
- **Application Status Search**:
  - Allows applicants to verify their application review status (`New`, `Under Verification`, `Verified`, `Confirmed`) using either their `CUTM-XXXXXX` Reference ID or 10-digit mobile number.
- **Admission Roadmap & Eligibility Breakdown**:
  - Detailed 4-step admission guide with clear criteria for each branch.

### 3. `courses.html` - Multi-Faculty Academic Program Directory
- **Departmental Filter Tabs**:
  - Instant filtering across Engineering, Polytechnic, Agriculture, Management, and Nursing.
- **Comprehensive Course Cards**:
  - Displays duration, seat matrix, annual fees, eligibility thresholds, laboratory specializations, and career opportunities.
- **Dynamic Fee Structure & Matrix**:
  - Clear, transparent fee tables for each program.

### 4. `dashboard.html` - Real-Time Administrative Counseling Hub
- **Reactive Background Auto-Polling**:
  - Checks `/leads` every 10 seconds without requiring manual page reloads.
- **Acoustic Audio Chime Alert**:
  - Synthesizes an alert chime via the modern Web Audio API whenever a new applicant applies.
- **Slide-in Real-Time Toast Banner**:
  - Displays instant notifications with applicant name and course.
- **Multi-Column Live Search & Multi-Tier Filter**:
  - Live search across Name, Mobile, Email, Ref ID, Course, and Status (`New`, `Contacted`, `Verified`, `Confirmed`, `Rejected`).
- **1-Click WhatsApp Web & Calling Outreach**:
  - Direct WhatsApp links (`wa.me`) with pre-composed counselor greeting messages and `tel:` links.
- **1-Click CSV / Excel Export**:
  - Generates downloadable CSV files (`CUTM_Admissions_List_YYYY-MM-DD.csv`).
- **Applicant Inspection Modal**:
  - Allows counselors to update statuses and add remarks.

### 5. `login.html` - Dual-Tab Portal Sign In & Registration
- **Dual-Tab Interface**:
  - Dedicated tabs for **Sign In** and **New Student Registration**.
- **Real-Time Client Validation**:
  - Validates passwords, emails, and phone formats.
- **Role-Based Redirection**:
  - Automatically redirects students to admissions/portal and administrators to `dashboard.html`.
- **Token Persistence**:
  - Securely stores the 24-hour JWT token in `localStorage`.

### 6. `gallery.html` - Campus Visual Tour
- High-definition photography covering lecture theaters, advanced robotics labs, EV workshops, agriculture polyhouses, and sports facilities.

### 7. `contact.html` & `overview.html`
- Addresses, phone numbers, and location details for Bhubaneswar, Parlakhemundi, Balangir, Rayagada, and Balasore campuses.
- University history, mission, leadership, and NAAC/UGC/AICTE/ICAR accreditation credentials.

---

## 🎨 UI/UX Design Tokens (`site.css`)

```css
:root {
    --navy: #102B4E;      /* Primary institutional navy */
    --blue: #1458A6;      /* Interactive blue accent */
    --gold: #EDAA32;      /* Prestige gold highlight */
    --ink:  #17283D;      /* High-contrast body typography */
    --muted: #64748B;     /* Subtitle and caption gray */
    --pale: #F4F7FB;      /* Background contrast surface */
    --line: #E4EAF1;      /* Border line delimiter */
    --shadow-card: 0 4px 18px rgba(16, 43, 78, 0.08);
}
```

---

## 📂 Frontend Folder Organization

```text
frontend/
├── admissions.html        # Online application & AI merit predictor page
├── contact.html           # Campus contact & maps page
├── courses.html           # Multi-faculty academic course directory
├── dashboard.html         # Real-time counselor dashboard with auto-polling & audio chime
├── gallery.html           # Visual tour & campus photography gallery
├── index.html             # CUTM university homepage with hero, highlights, & AI chat
├── login.html             # Dual-tab Sign In and New Student Registration page
├── overview.html          # University background, history & accreditation page
├── site.css               # Main institutional stylesheet
├── README.md              # Frontend documentation
├── css/
│   └── site.css           # Mirrored stylesheet for relative imports
├── js/
│   └── main.js            # Shared client authentication & formatting utilities
└── images/
    ├── cutm_logo.png      # Official circular CUTM emblem seal
    ├── cutm_campus_hero.jpg # Panoramic campus photograph
    └── ...                # Campus photo gallery assets
```

