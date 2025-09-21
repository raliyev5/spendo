from fastapi import APIRouter
from app.schemas.periods import PeriodIn
from app.services import periods_svc

router = APIRouter()

@router.get("/periods")
def list_periods():
    return periods_svc.list_periods()

@router.post("/periods")
def upsert_period(p: PeriodIn):
    return periods_svc.upsert_period(p.ym)

@router.post("/periods/{pid}/lock")
def lock_period(pid: int):
    return periods_svc.lock(pid, True)

@router.post("/periods/{pid}/unlock")
def unlock_period(pid: int):
    return periods_svc.lock(pid, False)
