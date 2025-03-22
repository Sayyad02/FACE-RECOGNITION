# database.py
import sqlite3
import numpy as np
import io
import config

def adapt_array(arr):
    """Converts a NumPy array to a binary string for database storage."""
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    """Converts a binary string from the database back to a NumPy array."""
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

# Register the adapters
sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("array", convert_array)

def create_database():
    """Creates the database and the faces table if they don't exist."""
    conn = sqlite3.connect(config.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            encoding array NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_face_to_db(name, encoding):
    """Adds a new face (name and encoding) to the database."""
    conn = sqlite3.connect(config.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO faces (name, encoding) VALUES (?, ?)", (name, encoding))
        conn.commit()
        print(f"Face '{name}' added to the database.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()



def get_all_faces_from_db():
    """Retrieves all face encodings and names from the database."""
    conn = sqlite3.connect(config.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name, encoding FROM faces")
        rows = cursor.fetchall()

        names = []
        encodings = []
        for row in rows:
            names.append(row[0])
            encodings.append(row[1])

        return names, encodings

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return [], []  # Return empty lists on error
    finally:
        conn.close()


def delete_face_from_db(name):
    """Deletes a face from the database by name."""
    conn = sqlite3.connect(config.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM faces WHERE name = ?", (name,))
        conn.commit()
        print(f"Face '{name}' deleted from the database.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def update_face_in_db(name, new_encoding):
    """Updates the encoding for an existing face in the database."""
    conn = sqlite3.connect(config.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE faces SET encoding = ? WHERE name = ?", (new_encoding, name))
        conn.commit()
        print(f"Encoding for face '{name}' updated in the database.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()