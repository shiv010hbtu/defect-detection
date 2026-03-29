import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "defects.db")


class DefectLogger:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inspections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                severity TEXT,
                defect_count INTEGER,
                confidence REAL,
                is_anomaly INTEGER,
                inspected_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save(self, filename, severity, defect_count, confidence, anomaly):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inspections (filename, severity, defect_count, confidence, is_anomaly, inspected_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (filename, severity, defect_count, confidence, int(anomaly), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

    def get_all(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inspections ORDER BY id DESC LIMIT 20")
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    def clear(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inspections")
        conn.commit()
        conn.close()
