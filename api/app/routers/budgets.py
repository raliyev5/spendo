from fastapi import APIRouter, Body
from app.schemas.budgets import BudgetLineIn, BudgetLinePatch, AllocationReplaceItem
from app.services import budgets_svc

router = APIRouter()

@router.get("/periods/{pid}/budgets")
def get_budgets(pid: int):
    return budgets_svc.get_budgets_of_period(pid)

@router.post("/budget-lines")
def create_budget_line(payload: BudgetLineIn):
    new_id = budgets_svc.create_budget_line(
        period_id=payload.period_id,
        category_id=payload.category_id,
        planned_cents=payload.planned_cents,
        bank_id=payload.bank_id,
        note=payload.note
    )
    return {"id": new_id}

@router.patch("/budget-lines/{bid}")
def patch_budget_line(bid: int, patch: BudgetLinePatch):
    fields = {k: v for k, v in patch.model_dump().items() if v is not None}
    return budgets_svc.patch_budget_line(bid, fields)

@router.delete("/budget-lines/{bid}")
def delete_budget_line(bid: int):
    return budgets_svc.delete_budget_line(bid)

@router.post("/budget-lines/{bid}/allocations/replace")
def replace_allocations(bid: int, items: list[AllocationReplaceItem] = Body(...)):
    tuples = [(it.category_id, it.amount_cents, it.bank_id, it.note) for it in items]
    return budgets_svc.replace_allocations(bid, tuples)
