from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes.dataset_routes import router as dataset_router
from .api.routes.report_routes import router as report_router
from .core.config import settings
from .core.middleware import RequestLoggingMiddleware
from .core.logging import setup_logging
from .db.models import Base
from .db.schema_repair import ensure_reports_table_columns
from .db.session import engine

setup_logging()

app = FastAPI(title="SentinelAI API")

app.add_middleware(RequestLoggingMiddleware)

cors_allow_origins = [
    origin.strip()
    for origin in settings.CORS_ALLOW_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origins,
    allow_origin_regex=settings.CORS_ALLOW_ORIGIN_REGEX,
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
