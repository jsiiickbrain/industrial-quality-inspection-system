import sqlite3
from datetime import datetime

DB_NAME = "inspection_data.db"

def init_db():
    """إنشاء جدول الفحوصات في حال لم يكن موجوداً"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inspection_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            item_id TEXT NOT NULL,
            status TEXT NOT NULL,
            confidence REAL,
            defect_type TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_inspection(item_id, status, confidence, defect_type="None"):
    """إضافة نتيجة فحص جديدة إلى قاعدة البيانات"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO inspection_logs (timestamp, item_id, status, confidence, defect_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, item_id, status, confidence, defect_type))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")