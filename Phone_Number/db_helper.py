import sqlite3
from pathlib import Path

DB_FILE = "checked.db"

def init_db():
    Path(DB_FILE).touch(exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS checked (
                phone TEXT PRIMARY KEY,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

def is_checked(phone):
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute("SELECT 1 FROM checked WHERE phone = ?", (phone,)).fetchone()
        return row is not None

def save_checked(phone, status="done"):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT OR IGNORE INTO checked (phone, status) VALUES (?, ?)", (phone, status))
