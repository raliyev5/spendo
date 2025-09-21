from pydantic import BaseModel
from typing import Literal, List

class PieItem(BaseModel):
    category_id: int
    category_name: str
    amount_cents: int

class PieResponse(BaseModel):
    period: str
    mode: Literal["top","expanded"]
    items: List[PieItem]

class BankRow(BaseModel):
    bank_id: int
    bank_name: str
    bank_code: str | None = None
    payments: int
    amount_cents: int

class BanksSummary(BaseModel):
    period: str
    total_payments: int
    total_amount_cents: int
    banks: list[BankRow]
