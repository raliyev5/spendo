from typing import Literal
from app.repositories import budgets_repo, categories_repo, periods_repo, banks_repo
from app.utils.dates import normalize_ym_str
from app.utils.errors import NotFound

def pie(period: str, mode: Literal["top","expanded"]="top"):
    ym = normalize_ym_str(period)
    p = periods_repo.get_period_by_ym(ym)
    if not p:
        raise NotFound("Period not found")
    pid = p[0]

    cats = categories_repo.fetch_all()
    code_by_id = {r[0]: r[2] for r in cats}
    name_by_id = {r[0]: r[1] for r in cats}

    lines = budgets_repo.fetch_all_lines_for_pie(pid)
    out: dict[int,int] = {}
    cc_line_ids: list[int] = []
    for lid, cid, planned in lines:
        planned = int(planned)
        if mode == "top":
            out[cid] = out.get(cid, 0) + planned
        else:
            if code_by_id.get(cid) == "credit_card":
                cc_line_ids.append(lid)
            else:
                out[cid] = out.get(cid, 0) + planned

    if mode == "expanded" and cc_line_ids:
        for cid, amount in budgets_repo.sum_allocations_by_category(cc_line_ids):
            out[cid] = out.get(cid, 0) + int(amount)
        # необязательный остаток кредитки опускаем

    items = [
        {"category_id": cid, "category_name": name_by_id.get(cid, f"cat:{cid}"), "amount_cents": amt}
        for cid, amt in sorted(out.items(), key=lambda kv: kv[1], reverse=True)
    ]
    return {"period": ym, "mode": mode, "items": items}

def banks_summary(period: str):
    ym = normalize_ym_str(period)
    p = periods_repo.get_period_by_ym(ym)
    if not p:
        raise NotFound("Period not found")
    pid = p[0]

    banks = {r[0]: {"bank_id": r[0], "bank_name": r[1], "bank_code": r[2], "payments": 0, "amount_cents": 0}
             for r in banks_repo.fetch_all()}

    for bank_id, amount in budgets_repo.non_cc_lines_by_bank(pid):
        if bank_id in banks:
            banks[bank_id]["payments"] += 1
            banks[bank_id]["amount_cents"] += int(amount)

    for bank_id, amount in budgets_repo.cc_allocations_by_bank(pid):
        if bank_id in banks:
            banks[bank_id]["payments"] += 1
            banks[bank_id]["amount_cents"] += int(amount)

    items = list(banks.values())
    total_payments = sum(b["payments"] for b in items)
    total_amount = sum(b["amount_cents"] for b in items)
    return {"period": ym, "total_payments": total_payments, "total_amount_cents": total_amount, "banks": items}
