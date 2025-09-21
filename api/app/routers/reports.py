from fastapi import APIRouter
from typing import Literal
from app.services import reports_svc

router = APIRouter()

@router.get("/reports/pie")
def report_pie(period: str, mode: Literal["top","expanded"]="top"):
    return reports_svc.pie(period, mode)

@router.get("/banks/summary")
def banks_summary(period: str):
    return reports_svc.banks_summary(period)
