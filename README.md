# Spendo

**Spendo** is a lightweight, containerized project for **personal and family budget planning**.  
It focuses on **monthly budgeting** (instead of tracking every single transaction), with flexible categorization, allocation rules (e.g., splitting credit card expenses by category), and visualization (pie charts, bank activity counters).

---

## 📖 Overview

- **Goal**: Plan a monthly budget (rent, groceries, credit card, etc.), track allocations, and get insights through reports.
- **Approach**: Instead of logging every coffee, the user defines **planned amounts per category per month**, and then splits allocations when needed (e.g., credit card into groceries/clothing).
- **Reports**: Pie charts, category breakdown, bank transaction counters.
- **Design**: Dark UI, similar to *dtf.ru* style.

---

## 🛠️ Technology Stack

| Layer      | Tech & Tools                                                   |
|------------|---------------------------------------------------------------|
| Backend    | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) with `uvloop` |
| Database   | PostgreSQL 16 (with tuned memory parameters)                   |
| Frontend   | [React](https://react.dev/) + [Vite](https://vite.dev/)        |
| Packaging  | [Docker](https://www.docker.com/) + Docker Compose             |
| Data Model | [Pydantic](https://docs.pydantic.dev/latest/) + `pydantic-settings` |

---

## 📂 Project Structure

```
spendo/
├── api/                   # Backend (Python/FastAPI)
│   ├── app/
│   │   ├── db/            # Database connection + migrations
│   │   ├── repositories/  # SQL queries & persistence layer
│   │   ├── routers/       # REST API endpoints
│   │   ├── schemas/       # Pydantic models (validation/serialization)
│   │   ├── services/      # Business logic
│   │   ├── utils/         # Utilities (errors, date normalization, etc.)
│   │   ├── factory.py     # Application factory
│   │   ├── settings.py    # Config (database URL, CORS, etc.)
│   │   └── main.py        # Legacy entrypoint (kept for reference)
│   ├── Dockerfile
│   └── requirements.txt
│
├── db/                    # PostgreSQL init scripts
│   └── 00_init.sql
│
├── web/                   # Frontend (React + Vite)
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml     # Orchestration (db, api, web)
└── README.md              # Project documentation
```

---

## 🚀 Running the Project

### Prerequisites
- Docker + Docker Compose installed
- Port availability:  
  - `5432` for PostgreSQL  
  - `8000` for FastAPI  
  - `3000` for React frontend  

### Quick Start
```bash
docker compose up --build
```

### Services

- **Backend API** → [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)  
- **Health check** → [http://localhost:8000/health](http://localhost:8000/health)  
- **Frontend** → [http://localhost:3000](http://localhost:3000)

---

## 📑 API Specification (MVP)

### Periods
- `GET /periods` → List available months
- `POST /periods` → Create or upsert month (format: `YYYY-MM`)
- `POST /periods/{id}/lock` → Lock a period (make immutable)
- `POST /periods/{id}/unlock` → Unlock a period

### Budgets
- `GET /periods/{id}/budgets` → Get monthly budget sheet
- `POST /budget-lines` → Add budget line
- `PATCH /budget-lines/{id}` → Update line
- `DELETE /budget-lines/{id}` → Remove line
- `POST /budget-lines/{id}/allocations/replace` → Replace allocations (sub-items)

### Reports
- `GET /reports/pie?period=YYYY-MM&mode=top|expanded`  
  - `top`: shows top-level categories  
  - `expanded`: unfolds allocations (e.g., credit card splits)
- `GET /banks/summary?period=YYYY-MM` → Count payments per bank (useful for “≥3 transactions” rule)

### Health
- `GET /health` → `{ "status": "ok" }`

---

## 💡 Design Principles

- **Simplicity first** → Start with monthly planning, not transaction-level tracking.  
- **Flexibility** → Credit card lines can be unfolded into sub-categories.  
- **Transparency** → Reports are designed to quickly answer: *“Where did the money go this month?”*  
- **Portability** → All services run in Docker, minimal setup required.  
- **Dark mode UI** → Inspired by `dtf.ru`, optimized for long daily use.

---

## 🔮 Roadmap

- [x] Periods CRUD (create/lock/unlock)  
- [x] Budget lines with allocations  
- [x] Reports: pie chart and banks summary  
- [ ] Editable frontend table (monthly sheet)  
- [ ] Interactive dark-theme UI with charts  
- [ ] Multi-user support with authentication  
- [ ] Extended analytics (yearly summary, trends, savings goals)  

---

## ⚙️ Development Workflow

### Rebuild & restart containers
```bash
docker compose build api web
docker compose up -d
```

### Check API logs
```bash
docker compose logs -f api
```

### Run SQL migrations manually
```bash
docker compose exec db psql -U spendo -d spendo
```

### Enter backend container
```bash
docker compose exec api sh
```
