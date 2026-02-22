from fastapi import FastAPI

from .api.routes.dataset_routes import router as dataset_router
from .api.routes.report_routes import router as report_router
from .core.middleware import RequestLoggingMiddleware
from .core.logging import setup_logging
from .db.models import Base
from .db.session import engine

setup_logging()

app = FastAPI(title="SentinelAI API")
app.add_middleware(RequestLoggingMiddleware)
app.include_router(dataset_router)
app.include_router(report_router)

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
