from app.api.routes.dataset_routes import router as dataset_router
from app.db.models import Base
from app.db.session import engine
from fastapi import FastAPI


app = FastAPI(title="SentinelAI API")
app.include_router(dataset_router)

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
