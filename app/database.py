import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "saas.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        notes TEXT DEFAULT '',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        duration INTEGER NOT NULL DEFAULT 30,
        price REAL NOT NULL DEFAULT 0,
        active INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'confirmed',
        notes TEXT DEFAULT '',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(service_id) REFERENCES services(id)
    );
    """)

    count = conn.execute("SELECT COUNT(*) FROM services").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO services (name, duration, price) VALUES (?, ?, ?)",
            [
                ("Haircut", 30, 199),
                ("Haircut + Beard", 45, 299),
                ("Hair Spa", 60, 499),
            ],
        )
    conn.commit()
    conn.close()
