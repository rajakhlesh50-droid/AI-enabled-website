# Engineering Rules, Standards & Conventions
## Centurion University of Technology and Management (CUTM)

---

### 1. General Principles
1. **Preserve Documentation & Context:** Never remove or overwrite existing business logic, route handlers, or database records without explicit user direction.
2. **Backward Compatibility First:** Any database migration or API enhancement must maintain compatibility with existing client scripts and database records.
3. **Encoding Discipline (Windows OS):**
   - Always run Python processes with UTF-8 encoding (`PYTHONIOENCODING=utf-8`).
   - Do not print non-ASCII raw symbols (like the ₹ Rupee symbol) directly to standard Windows cmd without UTF-8 reconfiguration to avoid `UnicodeEncodeError`.

---

### 2. Backend Coding Standards (Python / Flask)

- **Architecture:** Keep endpoints lean. Move reusable business calculations (such as lead merit scoring, AI evaluation, and password handling) into dedicated modules (`src/scoring.py`, `src/auth.py`).
- **RESTful Conventions:**
  - `GET` requests must be idempotent and perform no mutations.
  - `POST` requests create resources and must return appropriate HTTP status (`201 Created` or `400 Bad Request`).
  - `PUT` requests update resources and return `200 OK`.
  - `DELETE` requests remove resources and return `200 OK` or `404 Not Found`.
- **Database Safety:**
  - Always use parameterized queries (`?`) to prevent SQL Injection.
  - Never concatenate raw user input into SQL query strings.
  - Set a 10-second connection timeout on SQLite connections: `sqlite3.connect(DATABASE_PATH, timeout=10)`.
- **Authentication & Passwords:**
  - Never store plain-text passwords in the database.
  - Always use `werkzeug.security.generate_password_hash` with default PBKDF2/scrypt salting.
  - Verify passwords via `werkzeug.security.check_password_hash`.
  - Issue JWT tokens signed with `HS256` containing standard claims: `user`, `role`, `name`, `exp`.

---

### 3. Frontend Standards (HTML / CSS / JavaScript)

- **Zero Heavy Framework Lock-in:** Use semantic HTML5, pure CSS3 variables, and modern vanilla JavaScript (ES6+ `async/await`, `fetch`, `Intl`).
- **XSS Prevention:**
  - Always sanitize dynamic HTML content before injecting into innerHTML using `escapeHtml()`:
    ```javascript
    function escapeHtml(value) {
        return String(value ?? "").replace(/[&<>"']/g, c => ({
            "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
        })[c]);
    }
    ```
- **Form Validation:**
  - Enforce both client-side HTML5 validation (`required`, `type="email"`, `pattern="[0-9]{10}"`) and server-side validation in Python.
- **Brand Consistency:**
  - Always use official CUTM circular logo (`images/cutm_logo.png`).
  - Keep primary header branding as: **Centurion University of Technology and Management (CUTM)**.

---

### 4. Git & Commit Guidelines
- Commit messages should be concise and declarative:
  - `feat: add dual-tab registration and login portal`
  - `style: update official circular CUTM emblem and favicon`
  - `fix: prevent UnicodeEncodeError in Windows terminal logs`
  - `docs: update system architecture and task logs`

