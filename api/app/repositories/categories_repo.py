from app.db.connection import get_cursor

def fetch_all() -> list[tuple]:
    with get_cursor() as cur:
        cur.execute("SELECT id, name, code FROM categories;")
        return cur.fetchall()
