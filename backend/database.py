"""
Centurion University of Technology and Management (CUTM)
Backend Database Layer - SQLite Relational Persistence
"""

import datetime
import json
import sqlite3
from werkzeug.security import generate_password_hash

try:
    from .config import DATABASE_PATH, DEFAULT_EVENTS
except ImportError:
    from config import DATABASE_PATH, DEFAULT_EVENTS


def get_db():
    """Returns an active SQLite database connection with row factory enabled."""
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db():
    """Initializes tables and seeds default records if not present."""
    with get_db() as connection:
        # 1. Events Table
        connection.execute(
            "CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, data TEXT NOT NULL)"
        )

        # 2. Event Registrations Table
        connection.execute(
            "CREATE TABLE IF NOT EXISTS event_registrations (id TEXT PRIMARY KEY, data TEXT NOT NULL)"
        )

        # 3. Admission Leads Table
        connection.execute(
            "CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL)"
        )

        # 4. App Settings Key-Value Store
        connection.execute(
            "CREATE TABLE IF NOT EXISTS app_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )

        # 5. User Accounts Table (Admins, Students)
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

        # Seed default administrator account if missing
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

        # Seed default campus events if missing
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


# -------------------------------------------------------------
# Event Data Helpers
# -------------------------------------------------------------
def list_event_documents():
    with get_db() as connection:
        rows = connection.execute("SELECT data FROM events").fetchall()
    event_documents = [json.loads(row["data"]) for row in rows]
    return sorted(event_documents, key=lambda event: event.get("date", ""))


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


def delete_event(event_id):
    with get_db() as connection:
        result = connection.execute("DELETE FROM events WHERE id = ?", (event_id,))
    return result.rowcount > 0


# -------------------------------------------------------------
# Registration Data Helpers
# -------------------------------------------------------------
def list_registration_documents():
    with get_db() as connection:
        rows = connection.execute(
            "SELECT data FROM event_registrations ORDER BY rowid DESC"
        ).fetchall()
    return [json.loads(row["data"]) for row in rows]


def create_registration(registration):
    with get_db() as connection:
        connection.execute(
            "INSERT INTO event_registrations (id, data) VALUES (?, ?)",
            (registration["id"], json.dumps(registration)),
        )


def delete_registration(registration_id):
    with get_db() as connection:
        result = connection.execute(
            "DELETE FROM event_registrations WHERE id = ?", (registration_id,)
        )
    return result.rowcount > 0


# -------------------------------------------------------------
# Lead & Admission Data Helpers
# -------------------------------------------------------------
def list_lead_documents():
    with get_db() as connection:
        rows = connection.execute("SELECT data FROM leads ORDER BY id DESC").fetchall()
    return [json.loads(row["data"]) for row in rows]


def insert_lead(lead_data):
    with get_db() as connection:
        cursor = connection.execute("INSERT INTO leads (data) VALUES (?)", (json.dumps(lead_data),))
        return cursor.lastrowid


def update_lead_by_phone(phone, updates):
    count = 0
    with get_db() as connection:
        rows = connection.execute("SELECT id, data FROM leads").fetchall()
        for row in rows:
            doc = json.loads(row["data"])
            if doc.get("phone") == phone:
                doc.update(updates)
                connection.execute(
                    "UPDATE leads SET data = ? WHERE id = ?",
                    (json.dumps(doc), row["id"]),
                )
                count += 1
    return count


def delete_leads_by_phone(phone):
    with get_db() as connection:
        rows = connection.execute("SELECT id, data FROM leads").fetchall()
        ids = [row["id"] for row in rows if json.loads(row["data"]).get("phone") == phone]
        connection.executemany("DELETE FROM leads WHERE id = ?", [(item,) for item in ids])
    return len(ids)


def find_lead_by_query(query):
    query = query.strip()
    with get_db() as connection:
        rows = connection.execute("SELECT data FROM leads ORDER BY id DESC").fetchall()
    for row in rows:
        lead_data = json.loads(row["data"])
        if lead_data.get("ref_id", "").upper() == query.upper() or lead_data.get("phone", "") == query:
            return lead_data
    return None


# -------------------------------------------------------------
# User Account Helpers
# -------------------------------------------------------------
def find_user_by_login(login_id):
    login_id = login_id.strip().lower()
    with get_db() as connection:
        return connection.execute(
            "SELECT * FROM users WHERE lower(username) = ? OR lower(email) = ?",
            (login_id, login_id)
        ).fetchone()


def check_existing_user(username, email):
    username = username.strip().lower()
    email = email.strip().lower()
    with get_db() as connection:
        return connection.execute(
            "SELECT id, username, email FROM users WHERE lower(username) = ? OR lower(email) = ?",
            (username, email)
        ).fetchone()


def create_user(username, email, phone, name, password_hash, role="student"):
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with get_db() as connection:
        cursor = connection.execute(
            "INSERT INTO users (username, email, phone, name, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, email, phone, name, password_hash, role, created_at)
        )
        return cursor.lastrowid

