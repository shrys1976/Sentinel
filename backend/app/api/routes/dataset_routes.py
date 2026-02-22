from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ...core.dependencies import RequestContext, get_request_context
from ...db.session import get_db
from ...schemas.dataset_schema import (
    DatasetHistoryItem,
    DatasetHistoryResponse,
    DatasetStatusResponse,
    DatasetUploadResponse,
)
from ...services.dataset_service import (
    create_dataset,
    get_dataset_status,
    get_datasets_for_user,
)
from ...utils.file_validation import (
    validate_csv_structure,
    validate_file_extension,
    validate_file_size,
)
from ...workers.analysis_worker import process_dataset

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/upload", response_model=DatasetUploadResponse)
def upload_dataset(
    background_tasks: BackgroundTasks,
    context: RequestContext = Depends(get_request_context),
    file: UploadFile = File(...),
    name: str | None = Form(default=None),
    dataset_name: str | None = Form(default=None),
    db: Session = Depends(get_db),
):
    resolved_name = (dataset_name or name or "").strip()
    if not resolved_name:
        raise HTTPException(status_code=422, detail="dataset_name is required")

    validate_file_extension(file)
    validate_file_size(file)
    validate_csv_structure(file)

    dataset = create_dataset(
        db=db,
        file=file,
        dataset_name=resolved_name,
        user_id=context.user_id,
        session_id=context.session_id,
    )

    background_tasks.add_task(process_dataset, dataset.id)

    return DatasetUploadResponse(
        dataset_id=dataset.id,
        rows=dataset.rows,
        columns=dataset.columns,
        status=dataset.status,
    )


@router.get("", response_model=DatasetHistoryResponse)
def dataset_history(
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
):
    datasets = get_datasets_for_user(db, context.user_id, context.session_id)
    response = [
        DatasetHistoryItem(
            dataset_id=d.id,
            name=d.name,
            status=d.status,
            rows=d.rows,
            columns=d.columns,
            created_at=str(d.created_at),
        )
        for d in datasets
    ]
    return DatasetHistoryResponse(datasets=response)


@router.get("/{dataset_id}/status", response_model=DatasetStatusResponse)
def dataset_status(
    dataset_id: str,
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
):
    dataset, status = get_dataset_status(
        db,
        dataset_id,
        context.user_id,
        context.session_id,
    )

    if status == "not_found":
        raise HTTPException(status_code=404, detail="Dataset not found")

    if status == "forbidden":
        raise HTTPException(status_code=403, detail="Access denied")

    return DatasetStatusResponse(
        dataset_id=dataset.id,
        status=dataset.status,
        rows=dataset.rows,
        columns=dataset.columns,
    )
