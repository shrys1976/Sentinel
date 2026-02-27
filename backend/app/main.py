import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

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


_cors_origin_re = re.compile(r"https?://(localhost|127\.0\.0\.1)(:\d+)?$|https://.*\.vercel\.app$")
_cors_allow_origin_set = set(cors_allow_origins)


def _is_allowed_origin(origin: str) -> bool:
    if origin in _cors_allow_origin_set:
        return True
    return bool(_cors_origin_re.match(origin))


@app.middleware("http")
async def ensure_cors_headers(request, call_next):
    origin = request.headers.get("origin")

    if origin and _is_allowed_origin(origin) and request.method == "OPTIONS":
        preflight = Response(status_code=204)
        preflight.headers["Access-Control-Allow-Origin"] = origin
        preflight.headers["Access-Control-Allow-Credentials"] = "true"
        preflight.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,PATCH,DELETE,OPTIONS"
        preflight.headers["Access-Control-Allow-Headers"] = request.headers.get(
            "access-control-request-headers", "*"
        )
        preflight.headers["Vary"] = "Origin"
        return preflight

    response = await call_next(request)

    if origin and _is_allowed_origin(origin):
        response.headers.setdefault("Access-Control-Allow-Origin", origin)
        response.headers.setdefault("Access-Control-Allow-Credentials", "true")
        response.headers.setdefault("Vary", "Origin")

    return response

app.include_router(dataset_router)
app.include_router(report_router)
app.include_router(plot_router)

Base.metadata.create_all(bind=engine)
ensure_reports_table_columns(engine)
ensure_datasets_table_columns(engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
