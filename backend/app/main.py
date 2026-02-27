from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes.dataset_routes import router as dataset_router
from .api.routes.plot_routes import router as plot_router
from .api.routes.report_routes import router as report_router
from .core.config import settings
from .core.middleware import RequestLoggingMiddleware
from .core.logging import setup_logging
from .db.models import Base
from .db.schema_repair import ensure_datasets_table_columns, ensure_reports_table_columns
from .db.session import engine

setup_logging()

app = FastAPI(title="SentinelAI API")

app.add_middleware(RequestLoggingMiddleware)

cors_allow_origins = [
    origin.strip()
    for origin in settings.CORS_ALLOW_ORIGINS.split(",")
    if origin.strip()
]

default_cors_regex = r"https?://(localhost|127\.0\.0\.1)(:\d+)?|https://.*\.vercel\.app"
configured_regex = (settings.CORS_ALLOW_ORIGIN_REGEX or "").strip()
if configured_regex:
    # Always include Vercel preview/prod domains even when env regex is customized.
    cors_allow_origin_regex = f"(?:{configured_regex})|(?:https://.*\\.vercel\\.app)"
else:
    cors_allow_origin_regex = default_cors_regex

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origins,
    allow_origin_regex=cors_allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dataset_router)
app.include_router(report_router)
app.include_router(plot_router)

Base.metadata.create_all(bind=engine)
ensure_reports_table_columns(engine)
ensure_datasets_table_columns(engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
