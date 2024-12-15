import sqlite3
import os
import threading
from pathlib import Path

# 현재 파일의 디렉토리를 기준으로 상대 경로 설정
CURRENT_DIR = Path(__file__).resolve().parent
DATABASE_URL = str(CURRENT_DIR / "data" / "knowledge.db")
_thread_local = threading.local()

def init_db():
    os.makedirs(os.path.dirname(DATABASE_URL), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        level INTEGER NOT NULL,
        tags TEXT NOT NULL,
        content TEXT,
        summary TEXT
    )
    """)
    
    conn.commit()
    conn.close()

def get_db():
    if not hasattr(_thread_local, "connection"):
        _thread_local.connection = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    return _thread_local.connection

# Initialize database when the module is imported
init_db()
