"""
Скрипт для наполнения базы данных рок-хитов для Рэйнбоу Дэш.
Версия: 2.0 — расширенная база > 150 песен.
Автор: MADAO81
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
    {"artist": "AC/DC", "song": "T.N.T.", "genre": "Hard Rock", "vibe": "мощный"},
    {"artist": "AC/DC", "song": "Dirty Deeds Done Dirt Cheap", "genre": "Hard Rock", "vibe": "драйвовый"},
    {"artist": "AC/DC", "song": "For Those About to Rock", "genre": "Hard Rock", "vibe": "эпичный"},

    # === Metallica ===
    {"artist": "Metallica", "song": "Enter Sandman", "genre": "Thrash Metal", "vibe": "заряжающий"},
    {"artist": "Metallica", "song": "Master of Puppets", "genre": "Thrash Metal", "vibe": "мощный"},
    {"artist": "Metallica", "song": "Nothing Else Matters", "genre": "Ballad", "vibe": "эпичный"},
    {"artist": "Metallica", "song": "The Unforgiven", "genre": "Ballad", "vibe": "эпичный"},
    {"artist": "Metallica", "song": "One", "genre": "Thrash Metal", "vibe": "мощный"},
    {"artist": "Metallica", "song": "Seek & Destroy", "genre": "Thrash Metal", "vibe": "драйвовый"},
    {"artist": "Metallica", "song": "Fade to Black", "genre": "Ballad", "vibe": "эпичный"},
    {"artist": "Metallica", "song": "Creeping Death", "genre": "Thrash Metal", "vibe": "мощный"},

    # === Motorhead ===
    {"artist": "Motorhead", "song": "Ace of Spades", "genre": "Speed Metal", "vibe": "драйвовый"},
    {"artist": "Motorhead", "song": "Overkill", "genre": "Speed Metal", "vibe": "мощный"},
    {"artist": "Motorhead", "song": "Bomber", "genre": "Speed Metal", "vibe": "эпичный"},
    {"artist": "Motorhead", "song": "Iron Fist", "genre": "Speed Metal", "vibe": "драйвовый"},

    # === Iron Maiden ===
    {"artist": "Iron Maiden", "song": "The Trooper", "genre": "Heavy Metal", "vibe": "эпичный"},
    {"artist": "Iron Maiden", "song": "Run to the Hills", "genre": "Heavy Metal", "vibe": "драйвовый"},
    {"artist": "Iron Maiden", "song": "Fear of the Dark", "genre": "Heavy Metal", "vibe": "мощный"},
    {"artist": "Iron Maiden", "song": "Hallowed Be Thy Name", "genre": "Heavy Metal", "vibe": "эпичный"},
    {"artist": "Iron Maiden", "song": "The Number of the Beast", "genre": "Heavy Metal", "vibe": "мощный"},

    # === Guns N' Roses ===
    {"artist": "Guns N' Roses", "song": "Sweet Child O' Mine", "genre": "Hard Rock", "vibe": "заряжающий"},
    {"artist": "Guns N' Roses", "song": "Welcome to the Jungle", "genre": "Hard Rock", "vibe": "мощный"},
    {"artist": "Guns N' Roses", "song": "November Rain", "genre": "Ballad", "vibe": "эпичный"},
    {"artist": "Guns N' Roses", "song": "Paradise City", "genre": "Hard Rock", "vibe": "драйвовый"},

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

    # === НОВЫЕ ИСПОЛНИТЕЛИ ===

    # --- Limp Bizkit ---
    {"artist": "Limp Bizkit", "song": "Rollin'", "genre": "Nu Metal", "vibe": "драйвовый"},
    {"artist": "Limp Bizkit", "song": "Break Stuff", "genre": "Nu Metal", "vibe": "мощный"},
    {"artist": "Limp Bizkit", "song": "Nookie", "genre": "Nu Metal", "vibe": "заряжающий"},

    # --- Bloodhound Gang ---
    {"artist": "Bloodhound Gang", "song": "The Bad Touch", "genre": "Alternative Rock", "vibe": "драйвовый"},
    {"artist": "Bloodhound Gang", "song": "Fire Water Burn", "genre": "Alternative Rock", "vibe": "заряжающий"},

    # --- Insane Clown Posse ---
    {"artist": "Insane Clown Posse", "song": "Chicken Huntin'", "genre": "Hip Hop", "vibe": "мощный"},
    {"artist": "Insane Clown Posse", "song": "Miracles", "genre": "Hip Hop", "vibe": "заряжающий"},

    # --- Five Finger Death Punch ---
    {"artist": "Five Finger Death Punch", "song": "Wrong Side of Heaven", "genre": "Metal", "vibe": "эпичный"},
    {"artist": "Five Finger Death Punch", "song": "Jekyll and Hyde", "genre": "Metal", "vibe": "мощный"},
    {"artist": "Five Finger Death Punch", "song": "Bad Company", "genre": "Metal", "vibe": "драйвовый"},

    # --- Black Sabbath ---
    {"artist": "Black Sabbath", "song": "Paranoid", "genre": "Heavy Metal", "vibe": "классический"},
    {"artist": "Black Sabbath", "song": "Iron Man", "genre": "Heavy Metal", "vibe": "мощный"},
    {"artist": "Black Sabbath", "song": "War Pigs", "genre": "Heavy Metal", "vibe": "эпичный"},

    # --- Ozzy Osbourne ---
    {"artist": "Ozzy Osbourne", "song": "Crazy Train", "genre": "Heavy Metal", "vibe": "драйвовый"},
    {"artist": "Ozzy Osbourne", "song": "Bark at the Moon", "genre": "Heavy Metal", "vibe": "мощный"},

    # --- Running Wild ---
    {"artist": "Running Wild", "song": "Under Jolly Roger", "genre": "Power Metal", "vibe": "эпичный"},
    {"artist": "Running Wild", "song": "Riding the Storm", "genre": "Power Metal", "vibe": "мощный"},

    # --- W.A.S.P. ---
    {"artist": "W.A.S.P.", "song": "Wild Child", "genre": "Heavy Metal", "vibe": "драйвовый"},
    {"artist": "W.A.S.P.", "song": "I Wanna Be Somebody", "genre": "Heavy Metal", "vibe": "мощный"},

    # --- Cinderella ---
    {"artist": "Cinderella", "song": "Nobody's Fool", "genre": "Hard Rock", "vibe": "эпичный"},
    {"artist": "Cinderella", "song": "Shake Me", "genre": "Hard Rock", "vibe": "драйвовый"},

    # --- Mötley Crüe ---
    {"artist": "Mötley Crüe", "song": "Dr. Feelgood", "genre": "Heavy Metal", "vibe": "драйвовый"},
    {"artist": "Mötley Crüe", "song": "Kickstart My Heart", "genre": "Heavy Metal", "vibe": "заряжающий"},
    {"artist": "Mötley Crüe", "song": "Home Sweet Home", "genre": "Ballad", "vibe": "эпичный"},

    # --- Manowar ---
    {"artist": "Manowar", "song": "Warriors of the World", "genre": "Power Metal", "vibe": "эпичный"},
    {"artist": "Manowar", "song": "Battle Hymn", "genre": "Power Metal", "vibe": "мощный"},

    # --- Nazareth ---
    {"artist": "Nazareth", "song": "Hair of the Dog", "genre": "Hard Rock", "vibe": "мощный"},
    {"artist": "Nazareth", "song": "Love Hurts", "genre": "Ballad", "vibe": "эпичный"},

    # --- Dropkick Murphys ---
    {"artist": "Dropkick Murphys", "song": "Shipping Up to Boston", "genre": "Celtic Punk", "vibe": "драйвовый"},
    {"artist": "Dropkick Murphys", "song": "Rose Tattoo", "genre": "Celtic Punk", "vibe": "заряжающий"},

    # --- Sex Pistols ---
    {"artist": "Sex Pistols", "song": "Anarchy in the U.K.", "genre": "Punk Rock", "vibe": "мощный"},
    {"artist": "Sex Pistols", "song": "God Save the Queen", "genre": "Punk Rock", "vibe": "драйвовый"},

    # --- Green Day ---
    {"artist": "Green Day", "song": "Basket Case", "genre": "Punk Rock", "vibe": "драйвовый"},
    {"artist": "Green Day", "song": "American Idiot", "genre": "Punk Rock", "vibe": "мощный"},
    {"artist": "Green Day", "song": "Wake Me Up When September Ends", "genre": "Punk Rock", "vibe": "эпичный"},

    # --- Blink-182 ---
    {"artist": "Blink-182", "song": "All the Small Things", "genre": "Pop Punk", "vibe": "заряжающий"},
    {"artist": "Blink-182", "song": "What's My Age Again?", "genre": "Pop Punk", "vibe": "драйвовый"},

    # --- Sum 41 ---
    {"artist": "Sum 41", "song": "Fat Lip", "genre": "Pop Punk", "vibe": "драйвовый"},
    {"artist": "Sum 41", "song": "In Too Deep", "genre": "Pop Punk", "vibe": "заряжающий"},

    # --- Bad Religion ---
    {"artist": "Bad Religion", "song": "21st Century Digital Boy", "genre": "Punk Rock", "vibe": "мощный"},
    {"artist": "Bad Religion", "song": "Infected", "genre": "Punk Rock", "vibe": "драйвовый"},

    # --- The Offspring ---
    {"artist": "The Offspring", "song": "Self Esteem", "genre": "Punk Rock", "vibe": "драйвовый"},
    {"artist": "The Offspring", "song": "Pretty Fly (For a White Guy)", "genre": "Punk Rock", "vibe": "заряжающий"},

    # --- System of a Down ---
    {"artist": "System of a Down", "song": "Chop Suey!", "genre": "Alternative Metal", "vibe": "мощный"},
    {"artist": "System of a Down", "song": "Toxicity", "genre": "Alternative Metal", "vibe": "эпичный"},
    {"artist": "System of a Down", "song": "B.Y.O.B.", "genre": "Alternative Metal", "vibe": "драйвовый"},

    # --- Drowning Pool ---
    {"artist": "Drowning Pool", "song": "Bodies", "genre": "Nu Metal", "vibe": "мощный"},
    {"artist": "Drowning Pool", "song": "Tear Away", "genre": "Nu Metal", "vibe": "драйвовый"},

    # --- Disturbed ---
    {"artist": "Disturbed", "song": "Down with the Sickness", "genre": "Nu Metal", "vibe": "мощный"},
    {"artist": "Disturbed", "song": "Stricken", "genre": "Nu Metal", "vibe": "драйвовый"},

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
