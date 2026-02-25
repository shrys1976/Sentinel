from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes.dataset_routes import router as dataset_router
from .api.routes.report_routes import router as report_router
from .core.middleware import RequestLoggingMiddleware
from .core.logging import setup_logging
from .db.models import Base
from .db.schema_repair import ensure_reports_table_columns
from .db.session import engine

setup_logging()

app = FastAPI(title="SentinelAI API")

app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dataset_router)
app.include_router(report_router)

Base.metadata.create_all(bind=engine)
ensure_reports_table_columns(engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
