import sqlite3

DB_NAME = "alerts.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            src_ip TEXT,
            dst_ip TEXT,
            bytes INTEGER,
            attack_type TEXT,
            risk_level TEXT,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_alert(src_ip, dst_ip, bytes_val, attack_type, risk_level, details):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO alerts (src_ip, dst_ip, bytes, attack_type, risk_level, details)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (src_ip, dst_ip, bytes_val, attack_type, risk_level, details))
    conn.commit()
    conn.close()

def get_recent_alerts(limit=50):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
