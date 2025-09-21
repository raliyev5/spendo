from pydantic import BaseModel
from typing import Optional, List

class BudgetLineIn(BaseModel):
    period_id: int
    category_id: int
    planned_cents: int
    bank_id: Optional[int] = None
    note: Optional[str] = None

class BudgetLinePatch(BaseModel):
    category_id: Optional[int] = None
    planned_cents: Optional[int] = None
    bank_id: Optional[int] = None
    note: Optional[str] = None

class AllocationReplaceItem(BaseModel):
    category_id: int
    amount_cents: int
    bank_id: Optional[int] = None
    note: Optional[str] = None

class AllocationOut(BaseModel):
    id: int
    budget_line_id: int
    category_id: int
    category_name: str
    bank_id: Optional[int] = None
    bank_name: Optional[str] = None
    amount_cents: int
    note: Optional[str] = None

class BudgetLineOut(BaseModel):
    id: int
    category_id: int
    category_name: str
    category_code: str | None = None
    bank_id: Optional[int] = None
    bank_name: Optional[str] = None
    planned_cents: int
    note: Optional[str] = None
    allocations: List[AllocationOut] = []

class BudgetsOfPeriodOut(BaseModel):
    period_id: int
    items: list[BudgetLineOut]
