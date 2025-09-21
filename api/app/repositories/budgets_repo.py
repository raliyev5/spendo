from typing import Optional, Iterable
from app.db.connection import get_cursor

def fetch_lines_of_period(pid: int) -> list[tuple]:
    with get_cursor() as cur:
        cur.execute("""
            SELECT bl.id, bl.category_id, c.name, c.code, bl.bank_id, b.name, bl.planned_cents, bl.note
            FROM budget_lines bl
            JOIN categories c ON c.id = bl.category_id
            LEFT JOIN banks b ON b.id = bl.bank_id
            WHERE bl.period_id = %s
            ORDER BY c.name, bl.id;
        """, (pid,))
        return cur.fetchall()

def fetch_allocs_for_lines(line_ids: Iterable[int]) -> list[tuple]:
    ids = list(line_ids)
    if not ids:
        return []
    with get_cursor() as cur:
        cur.execute("""
            SELECT a.id, a.budget_line_id, a.category_id, c.name, a.bank_id, b.name, a.amount_cents, a.note
            FROM budget_allocations a
            JOIN categories c ON c.id = a.category_id
            LEFT JOIN banks b ON b.id = a.bank_id
            WHERE a.budget_line_id = ANY(%s)
            ORDER BY a.id;
        """, (ids,))
        return cur.fetchall()

def insert_budget_line(period_id: int, category_id: int, planned_cents: int,
                       bank_id: Optional[int], note: Optional[str]) -> int:
    with get_cursor() as cur:
        cur.execute("""
            INSERT INTO budget_lines (period_id, category_id, bank_id, planned_cents, note)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (period_id, category_id, bank_id, planned_cents, note))
        return cur.fetchone()[0]

def get_period_id_of_line(bid: int) -> Optional[int]:
    with get_cursor() as cur:
        cur.execute("SELECT period_id FROM budget_lines WHERE id=%s;", (bid,))
        row = cur.fetchone()
        return row[0] if row else None

def get_planned_of_line(bid: int) -> Optional[int]:
    with get_cursor() as cur:
        cur.execute("SELECT planned_cents FROM budget_lines WHERE id=%s;", (bid,))
        row = cur.fetchone()
        return int(row[0]) if row else None

def update_budget_line(bid: int, fields: dict) -> bool:
    if not fields:
        return True
    cols = []
    vals = []
    for k, v in fields.items():
        cols.append(f"{k}=%s")
        vals.append(v)
    with get_cursor() as cur:
        cur.execute(f"UPDATE budget_lines SET {', '.join(cols)} WHERE id=%s RETURNING id;", (*vals, bid))
        return cur.fetchone() is not None

def delete_budget_line(bid: int) -> None:
    with get_cursor() as cur:
        cur.execute("DELETE FROM budget_lines WHERE id=%s;", (bid,))

def replace_allocations(bid: int, items: list[tuple[int,int,Optional[int],Optional[str]]]) -> int:
    with get_cursor() as cur:
        cur.execute("DELETE FROM budget_allocations WHERE budget_line_id=%s;", (bid,))
        if items:
            cur.executemany("""
                INSERT INTO budget_allocations (budget_line_id, category_id, bank_id, amount_cents, note)
                VALUES (%s,%s,%s,%s,%s);
            """, [(bid, cat, bank, amt, note) for (cat, amt, bank, note) in items])
        # вернуть total
        cur.execute("SELECT COALESCE(SUM(amount_cents),0)::bigint FROM budget_allocations WHERE budget_line_id=%s;", (bid,))
        return int(cur.fetchone()[0])

def sum_allocations_by_category(line_ids: list[int]) -> list[tuple]:
    if not line_ids:
        return []
    with get_cursor() as cur:
        cur.execute("""
            SELECT a.category_id, SUM(a.amount_cents)::bigint
            FROM budget_allocations a
            WHERE a.budget_line_id = ANY(%s)
            GROUP BY a.category_id;
        """, (line_ids,))
        return cur.fetchall()

def non_cc_lines_by_bank(pid: int) -> list[tuple]:
    with get_cursor() as cur:
        cur.execute("""
            SELECT bl.bank_id, bl.planned_cents
            FROM budget_lines bl
            JOIN categories c ON c.id = bl.category_id
            WHERE bl.period_id=%s AND bl.bank_id IS NOT NULL AND COALESCE(c.code,'') <> 'credit_card';
        """, (pid,))
        return cur.fetchall()

def cc_allocations_by_bank(pid: int) -> list[tuple]:
    with get_cursor() as cur:
        cur.execute("""
            SELECT a.bank_id, a.amount_cents
            FROM budget_allocations a
            JOIN budget_lines bl ON bl.id = a.budget_line_id
            JOIN categories c ON c.id = bl.category_id
            WHERE bl.period_id=%s AND COALESCE(c.code,'')='credit_card' AND a.bank_id IS NOT NULL;
        """, (pid,))
        return cur.fetchall()

def fetch_all_lines_for_pie(pid: int) -> list[tuple]:
    with get_cursor() as cur:
        cur.execute("SELECT id, category_id, planned_cents FROM budget_lines WHERE period_id=%s;", (pid,))
        return cur.fetchall()
