from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.dataset_schema import DatasetUploadResponse
from app.services.dataset_service import create_dataset

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/upload", response_model=DatasetUploadResponse)
def upload_dataset(
    file: UploadFile = File(...),
    dataset_name: str = Form(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files supported.")

    dataset = create_dataset(db=db, file=file, dataset_name=dataset_name)

    return DatasetUploadResponse(
        dataset_id=dataset.id,
        rows=dataset.rows,
        columns=dataset.columns,
        status=dataset.status,
    )
