from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://spendo:spendo@db:5432/spendo")

app = FastAPI(title="Spendo API", version="0.1.0")

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True)

class PeriodIn(BaseModel):
    ym: str  # "YYYY-MM" или "YYYY-MM-01"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/periods")
def list_periods():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, ym::text, is_locked FROM periods ORDER BY ym DESC;")
        rows = cur.fetchall()
    return [{"id": r[0], "ym": r[1], "is_locked": r[2]} for r in rows]

@app.post("/periods")
def upsert_period(p: PeriodIn):
    # нормализуем к первому дню месяца
    try:
        parts = p.ym.split("-")
        ym_norm = f"{parts[0]}-{parts[1]}-01" if len(parts) == 2 else p.ym
    except Exception:
        raise HTTPException(400, "Invalid ym")
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO periods(ym,is_locked) VALUES (DATE %s, FALSE) "
            "ON CONFLICT (ym) DO UPDATE SET ym=EXCLUDED.ym RETURNING id, ym::text, is_locked;",
            (ym_norm,)
        )
        row = cur.fetchone()
    return {"id": row[0], "ym": row[1], "is_locked": row[2]}

@app.post("/periods/{pid}/lock")
def lock_period(pid: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE periods SET is_locked=TRUE WHERE id=%s RETURNING id;", (pid,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(404, "Period not found")
    return {"ok": True}

@app.post("/periods/{pid}/unlock")
def unlock_period(pid: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE periods SET is_locked=FALSE WHERE id=%s RETURNING id;", (pid,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(404, "Period not found")
    return {"ok": True}
