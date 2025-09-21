from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from app.routers import health, periods, budgets, reports

def create_app() -> FastAPI:
    app = FastAPI(title=settings.api_title, version=settings.api_version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(periods.router)
    app.include_router(budgets.router)
    app.include_router(reports.router)

    return app
