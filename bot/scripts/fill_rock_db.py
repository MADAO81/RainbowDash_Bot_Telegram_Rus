"""
Скрипт для наполнения базы данных рок-хитов для Рэйнбоу Дэш.

Автор: MADAO81
Версия: 1.0
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "rock_songs.db"

SONGS = [
    # === AC/DC ===
    {"artist": "AC/DC", "song": "Back in Black", "genre": "Hard Rock", "vibe": "мощный"},
    {"artist": "AC/DC", "song": "Thunderstruck", "genre": "Hard Rock", "vibe": "драйвовый"},
    {"artist": "AC/DC", "song": "Hells Bells", "genre": "Hard Rock", "vibe": "эпичный"},
    {"artist": "AC/DC", "song": "You Shook Me All Night Long", "genre": "Hard Rock", "vibe": "заряжающий"},
    {"artist": "AC/DC", "song": "Highway to Hell", "genre": "Hard Rock", "vibe": "драйвовый"},
    
    # === Metallica ===
    {"artist": "Metallica", "song": "Enter Sandman", "genre": "Thrash Metal", "vibe": "заряжающий"},
    {"artist": "Metallica", "song": "Master of Puppets", "genre": "Thrash Metal", "vibe": "мощный"},
    {"artist": "Metallica", "song": "Nothing Else Matters", "genre": "Ballad", "vibe": "эпичный"},
    {"artist": "Metallica", "song": "The Unforgiven", "genre": "Ballad", "vibe": "эпичный"},
    {"artist": "Metallica", "song": "One", "genre": "Thrash Metal", "vibe": "мощный"},
    
    # === Motorhead ===
    {"artist": "Motorhead", "song": "Ace of Spades", "genre": "Speed Metal", "vibe": "драйвовый"},
    {"artist": "Motorhead", "song": "Overkill", "genre": "Speed Metal", "vibe": "мощный"},
    {"artist": "Motorhead", "song": "Bomber", "genre": "Speed Metal", "vibe": "эпичный"},
    
    # === Iron Maiden ===
    {"artist": "Iron Maiden", "song": "The Trooper", "genre": "Heavy Metal", "vibe": "эпичный"},
    {"artist": "Iron Maiden", "song": "Run to the Hills", "genre": "Heavy Metal", "vibe": "драйвовый"},
    {"artist": "Iron Maiden", "song": "Fear of the Dark", "genre": "Heavy Metal", "vibe": "мощный"},
    
    # === Guns N' Roses ===
    {"artist": "Guns N' Roses", "song": "Sweet Child O' Mine", "genre": "Hard Rock", "vibe": "заряжающий"},
    {"artist": "Guns N' Roses", "song": "Welcome to the Jungle", "genre": "Hard Rock", "vibe": "мощный"},
    {"artist": "Guns N' Roses", "song": "November Rain", "genre": "Ballad", "vibe": "эпичный"},
    
    # === Queen ===
    {"artist": "Queen", "song": "Bohemian Rhapsody", "genre": "Rock", "vibe": "эпичный"},
    {"artist": "Queen", "song": "We Will Rock You", "genre": "Rock", "vibe": "заряжающий"},
    {"artist": "Queen", "song": "We Are the Champions", "genre": "Rock", "vibe": "мощный"},
    
    # === Deep Purple ===
    {"artist": "Deep Purple", "song": "Smoke on the Water", "genre": "Hard Rock", "vibe": "классический"},
    {"artist": "Deep Purple", "song": "Highway Star", "genre": "Hard Rock", "vibe": "драйвовый"},
    
    # === Led Zeppelin ===
    {"artist": "Led Zeppelin", "song": "Stairway to Heaven", "genre": "Rock", "vibe": "эпичный"},
    {"artist": "Led Zeppelin", "song": "Whole Lotta Love", "genre": "Rock", "vibe": "мощный"},
    
    # === The Rolling Stones ===
    {"artist": "The Rolling Stones", "song": "(I Can't Get No) Satisfaction", "genre": "Rock", "vibe": "драйвовый"},
    {"artist": "The Rolling Stones", "song": "Paint It Black", "genre": "Rock", "vibe": "мощный"},
    
    # === Nirvana ===
    {"artist": "Nirvana", "song": "Smells Like Teen Spirit", "genre": "Grunge", "vibe": "мощный"},
    {"artist": "Nirvana", "song": "Come as You Are", "genre": "Grunge", "vibe": "заряжающий"},
    
    # === Foo Fighters ===
    {"artist": "Foo Fighters", "song": "Everlong", "genre": "Rock", "vibe": "заряжающий"},
    {"artist": "Foo Fighters", "song": "The Pretender", "genre": "Rock", "vibe": "мощный"},
    
    # === Linkin Park ===
    {"artist": "Linkin Park", "song": "In the End", "genre": "Nu Metal", "vibe": "эпичный"},
    {"artist": "Linkin Park", "song": "Numb", "genre": "Nu Metal", "vibe": "мощный"},
    
    # === Rammstein ===
    {"artist": "Rammstein", "song": "Du Hast", "genre": "Industrial Metal", "vibe": "мощный"},
    {"artist": "Rammstein", "song": "Sonne", "genre": "Industrial Metal", "vibe": "эпичный"},
    
    # === The White Stripes ===
    {"artist": "The White Stripes", "song": "Seven Nation Army", "genre": "Garage Rock", "vibe": "драйвовый"},
    
    # === Pony Rock (эксклюзив) ===
    {"artist": "Rainbow Rock", "song": "Rarity's Theme", "genre": "Rock", "vibe": "эпичный"},
    {"artist": "Rainbow Rock", "song": "Twilight's Magic", "genre": "Rock", "vibe": "мощный"},
    {"artist": "Rainbow Rock", "song": "Pinkie's Party", "genre": "Rock", "vibe": "заряжающий"},
]

def fill_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    inserted = 0
    for song in SONGS:
        cursor.execute("""
            INSERT INTO rock_songs (artist, song, genre, vibe)
            VALUES (?, ?, ?, ?)
        """, (
            song['artist'],
            song['song'],
            song['genre'],
            song['vibe']
        ))
        inserted += 1

    conn.commit()
    conn.close()
    print(f"✅ Добавлено {inserted} песен в базу данных: {DB_PATH}")

if __name__ == "__main__":
    fill_db()
