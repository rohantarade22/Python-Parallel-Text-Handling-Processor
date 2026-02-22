import sqlite3
from datetime import datetime
import os

DB_PATH = "database/processor.db"

def create_database():
    if not os.path.exists("database"):
        os.makedirs("database")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text_chunk TEXT,
        sentiment_score INTEGER,
        tags TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_text(text, score, tags):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO texts (text_chunk, sentiment_score, tags, created_at)
    VALUES (?, ?, ?, ?)
    """, (text, score, tags, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()