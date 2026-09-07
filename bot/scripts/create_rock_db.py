"""
Скрипт для создания базы данных рок-хитов для Рэйнбоу Дэш.

Автор: MADAO81
Версия: 1.0
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "rock_songs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rock_songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT NOT NULL,
            song TEXT NOT NULL,
            genre TEXT,
            vibe TEXT
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_vibe ON rock_songs (vibe)")

    conn.commit()
    conn.close()
    print(f"✅ База данных рок-хитов создана: {DB_PATH}")

if __name__ == "__main__":
    init_db()
