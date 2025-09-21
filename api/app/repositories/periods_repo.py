from typing import Optional
from app.db.connection import get_cursor

def list_periods() -> list[tuple]:
    with get_cursor() as cur:
        cur.execute("SELECT id, ym::text, is_locked FROM periods ORDER BY ym DESC;")
        return cur.fetchall()

def upsert_period(ym_norm: str) -> tuple:
    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO periods(ym,is_locked) VALUES (DATE %s, FALSE) "
            "ON CONFLICT (ym) DO UPDATE SET ym=EXCLUDED.ym RETURNING id, ym::text, is_locked;",
            (ym_norm,)
        )
        return cur.fetchone()

def get_period(pid: int) -> Optional[tuple]:
    with get_cursor() as cur:
        cur.execute("SELECT id, ym::date, is_locked FROM periods WHERE id=%s;", (pid,))
        return cur.fetchone()

def get_period_by_ym(ym_norm: str) -> Optional[tuple]:
    with get_cursor() as cur:
        cur.execute("SELECT id, ym::date, is_locked FROM periods WHERE ym=DATE %s;", (ym_norm,))
        return cur.fetchone()

def set_lock(pid: int, locked: bool) -> bool:
    with get_cursor() as cur:
        cur.execute("UPDATE periods SET is_locked=%s WHERE id=%s RETURNING id;", (locked, pid))
        return cur.fetchone() is not None
