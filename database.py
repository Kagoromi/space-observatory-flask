import sqlite3

DATABASE_NAME = "database.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_space_objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            external_id TEXT UNIQUE,
            title TEXT NOT NULL,
            center TEXT,
            date_created TEXT,
            notes TEXT DEFAULT 'No notes',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    connection.commit()
    connection.close()

def get_all_items(search_query=None):
    connection = get_connection()
    if search_query:
        query_param = f"%{search_query}%"
        items = connection.execute(
            "SELECT * FROM saved_space_objects WHERE title LIKE ? OR center LIKE ? ORDER BY id DESC",
            (query_param, query_param)
        ).fetchall()
    else:
        items = connection.execute(
            "SELECT * FROM saved_space_objects ORDER BY id DESC"
        ).fetchall()
    connection.close()
    return items

def get_item_by_id(item_id):
    connection = get_connection()
    item = connection.execute(
        "SELECT * FROM saved_space_objects WHERE id = ?", 
        (item_id,)
    ).fetchone()
    connection.close()
    return item

def get_item_by_external_id(external_id):
    connection = get_connection()
    item = connection.execute(
        "SELECT * FROM saved_space_objects WHERE external_id = ?", 
        (external_id,)
    ).fetchone()
    connection.close()
    return item

def add_item(external_id, title, center, date_created, notes="No notes"):
    connection = get_connection()
    try:
        connection.execute("""
            INSERT INTO saved_space_objects (external_id, title, center, date_created, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (external_id, title, center, date_created, notes))
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        connection.close()
        return False

def update_item(item_id, notes, title=None, center=None):
    connection = get_connection()
    if title and center:
        connection.execute("""
            UPDATE saved_space_objects 
            SET notes = ?, title = ?, center = ?
            WHERE id = ?
        """, (notes, title, center, item_id))
    else:
        connection.execute("""
            UPDATE saved_space_objects 
            SET notes = ?
            WHERE id = ?
        """, (notes, item_id))
    connection.commit()
    connection.close()

def delete_item(item_id):
    connection = get_connection()
    connection.execute("DELETE FROM saved_space_objects WHERE id = ?", (item_id,))
    connection.commit()
    connection.close()