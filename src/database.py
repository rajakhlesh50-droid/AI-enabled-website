import datetime
import json
import sqlite3
from werkzeug.security import generate_password_hash
from .config import DATABASE_PATH, DEFAULT_EVENTS

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

