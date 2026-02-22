from fastapi import FastAPI

from .api.routes.dataset_routes import router as dataset_router
from .db.models import Base
from .db.session import engine
from .api.routes.report_routes import router as report_router


app = FastAPI(title="SentinelAI API")
app.include_router(dataset_router)
app.include_router(report_router)

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
