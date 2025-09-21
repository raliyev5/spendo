from app.repositories import periods_repo
from app.utils.dates import normalize_ym_str
from app.utils.errors import NotFound, Conflict

def list_periods():
    rows = periods_repo.list_periods()
    return [{"id": r[0], "ym": r[1], "is_locked": r[2]} for r in rows]

def upsert_period(ym: str):
    ym_norm = normalize_ym_str(ym)
    r = periods_repo.upsert_period(ym_norm)
    return {"id": r[0], "ym": r[1], "is_locked": r[2]}

def lock(pid: int, locked: bool = True):
    ok = periods_repo.set_lock(pid, locked)
    if not ok:
        raise NotFound("Period not found")
    return {"ok": True}

def ensure_not_locked(pid: int):
    p = periods_repo.get_period(pid)
    if not p:
        raise NotFound("Period not found")
    if p[2]:
        raise Conflict("Period is locked")

def get_by_ym(ym: str):
    ym_norm = normalize_ym_str(ym)
    p = periods_repo.get_period_by_ym(ym_norm)
    if not p:
        raise NotFound("Period not found")
    return {"id": p[0], "ym": str(p[1]), "is_locked": p[2]}
