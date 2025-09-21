from pydantic import BaseModel

class PeriodIn(BaseModel):
    ym: str  # "YYYY-MM" or "YYYY-MM-01"

class PeriodOut(BaseModel):
    id: int
    ym: str
    is_locked: bool
