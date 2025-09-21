from typing import Optional
from app.repositories import budgets_repo, periods_repo
from app.utils.errors import NotFound, Conflict, BadRequest

def get_budgets_of_period(pid: int):
    if not periods_repo.get_period(pid):
        raise NotFound("Period not found")
    lines = budgets_repo.fetch_lines_of_period(pid)
    out = [{
        "id": r[0], "category_id": r[1], "category_name": r[2], "category_code": r[3],
        "bank_id": r[4], "bank_name": r[5], "planned_cents": int(r[6]), "note": r[7],
        "allocations": []
    } for r in lines]
    id_to_idx = {ln["id"]: i for i, ln in enumerate(out)}
    allocs = budgets_repo.fetch_allocs_for_lines(id_to_idx.keys())
    for a in allocs:
        alloc = {
            "id": a[0], "budget_line_id": a[1], "category_id": a[2], "category_name": a[3],
            "bank_id": a[4], "bank_name": a[5], "amount_cents": int(a[6]), "note": a[7]
        }
        idx = id_to_idx.get(a[1])
        if idx is not None:
            out[idx]["allocations"].append(alloc)
    return {"period_id": pid, "items": out}

def create_budget_line(period_id: int, category_id: int, planned_cents: int,
                       bank_id: Optional[int], note: Optional[str]) -> int:
    p = periods_repo.get_period(period_id)
    if not p:
        raise NotFound("Period not found")
    if p[2]:
        raise Conflict("Period is locked")
    return budgets_repo.insert_budget_line(period_id, category_id, planned_cents, bank_id, note)

def patch_budget_line(bid: int, fields: dict):
    pid = budgets_repo.get_period_id_of_line(bid)
    if pid is None:
        raise NotFound("Budget line not found")
    p = periods_repo.get_period(pid)
    if p[2]:
        raise Conflict("Period is locked")
    ok = budgets_repo.update_budget_line(bid, fields)
    if not ok:
        raise NotFound("Budget line not found")
    return {"ok": True}

def delete_budget_line(bid: int):
    pid = budgets_repo.get_period_id_of_line(bid)
    if pid is None:
        raise NotFound("Budget line not found")
    p = periods_repo.get_period(pid)
    if p[2]:
        raise Conflict("Period is locked")
    budgets_repo.delete_budget_line(bid)
    return {"ok": True}

def replace_allocations(bid: int, items: list[tuple[int,int,Optional[int],Optional[str]]]):
    pid = budgets_repo.get_period_id_of_line(bid)
    if pid is None:
        raise NotFound("Budget line not found")
    p = periods_repo.get_period(pid)
    if p[2]:
        raise Conflict("Period is locked")
    planned = budgets_repo.get_planned_of_line(bid)
    if planned is None:
        raise NotFound("Budget line not found")
    total = sum(it[1] for it in items)
    if total > planned:
        raise BadRequest(f"Allocations total {total} exceeds planned {planned}")
    total_after = budgets_repo.replace_allocations(bid, items)
    return {"ok": True, "total_allocated": total_after}
