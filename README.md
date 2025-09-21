# Spendo

Spendo is a lightweight **personal/family budget planner** focused on **monthly planning** instead of tracking every single expense.  
You decide once a month how much to allocate for categories like *Rent*, *Groceries*, *Credit Card*, etc.  
Spendo helps you:
- lock monthly budgets once they’re set,
- split special categories (like *Credit Card*) into sub-allocations (e.g. Groceries 5k, Clothes 2k),
- see expenses as **top-level categories** or **expanded by subcategories**,
- track which bank accounts were used (with rules like *≥3 payments per bank per month*),
- generate visual reports (e.g. pie chart of categories vs. income).

---

## Features (MVP)

- **Periods (Months)**  
  Each month (`period`) can be created, filled with planned incomes/expenses, and locked.

- **Budgets**  
  Plan amounts per category and optionally assign them to a bank account.

- **Credit Card category with allocations**  
  A budget line can contain detailed allocations (sub-categories).  
  Reports can show:
  - *Top mode*: Credit Card as one slice,
  - *Expanded mode*: allocations merged into their subcategories.

- **Banks & counters**  
  Assign categories/allocations to specific banks.  
  Track number of payments per bank vs. the monthly goal (≥3).

- **Reports**  
  - Pie chart of categories (top or expanded mode),
  - Monthly/Yearly summaries,
  - Bank usage summary.

---

## Tech Stack

- **Backend**
  - [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) with `uvloop`
  - Database: **PostgreSQL** (tuned for low memory)
  - SQL schema managed via init scripts (later migrations with Alembic)
  - Libraries: `psycopg`, `pydantic`

- **Frontend**
  - [React](https://react.dev/) + [Vite](https://vitejs.dev/)
  - Dark UI design (inspired by dtf.ru)
  - Minimal Tailwind-like styling (manual for now)

- **Containerization**
  - [Docker Compose](https://docs.docker.com/compose/) orchestrates:
    - `db` (Postgres with init schema),
    - `api` (FastAPI app),
    - `web` (React frontend).

---

## Project Structure

