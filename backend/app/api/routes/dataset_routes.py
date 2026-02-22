from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...schemas.dataset_schema import DatasetUploadResponse
from ...services.dataset_service import create_dataset
from ...workers.analysis_worker import process_dataset

from app.schemas.dataset_schema import (
    DatasetHistoryResponse,
    DatasetHistoryItem
)

from app.services.dataset_service import (
    get_datasets_for_user
)

from app.core.dependencies import (

    get_request_context,
    RequestContext

)

from app.utils.file_validation import (

    validate_file_extension,

    validate_file_size,

    validate_csv_structure

)

from app.schemas.dataset_schema import(
    DatasetStatusResponse
)
from app.services.dataset_service import(
    get_dataset_status
)


router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/upload", response_model=DatasetUploadResponse)
def upload_dataset(

    background_tasks: BackgroundTasks,
    file: UploadFile | None = File(default=None),
   # csv_file: UploadFile | None = File(default=None),
   # dataset_name: str | None = Form(default=None),
    name: str | None = Form(default=None),
   # datasetName: str | None = Form(default=None),
    db: Session = Depends(get_db),
):
    upload_file = file 
    resolved_name =  name

    if upload_file is None:
        raise HTTPException(status_code=422, detail="file is required")
    if not resolved_name:
        raise HTTPException(status_code=422, detail="dataset_name is required")

    if not upload_file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files supported.")

    dataset = create_dataset(db=db, file=upload_file, dataset_name=resolved_name)

    # Queue async-style background processing after dataset exists.
    background_tasks.add_task(process_dataset, dataset.id)

    validate_file_extension(file)
    validate_file_size(file)
    validate_csv_structure(file)

    return DatasetUploadResponse(
        dataset_id=dataset.id,
        rows=dataset.rows,
        columns=dataset.columns,
        status=dataset.status,
    )


@router.get(

    "",
    response_model=DatasetHistoryResponse

)

def dataset_history(

    context: RequestContext = Depends(
        get_request_context
    ),

    db: Session = Depends(get_db)

):

    datasets = get_datasets_for_user(

        db,
        context.user_id,
        context.session_id

    )
    response = [

        DatasetHistoryItem(

            dataset_id=d.id,
            name=d.name,
            status=d.status,
            rows=d.rows,
            columns=d.columns,
            created_at=str(d.created_at)

        )
        for d in datasets
    ]

    return DatasetHistoryResponse(
        datasets=response

    )

@router.get(

    "/{dataset_id}/status",

    response_model=DatasetStatusResponse

)

def dataset_status(

    dataset_id: str,

    context: RequestContext = Depends(

        get_request_context

    ),

    db: Session = Depends(get_db)

):

    dataset, status = get_dataset_status(

        db,

        dataset_id,

        context.user_id,

        context.session_id

    )


    if status == "not_found":

        raise HTTPException(

            status_code=404,

            detail="Dataset not found"

        )


    if status == "forbidden":

        raise HTTPException(

            status_code=403,

            detail="Access denied"

        )


    return DatasetStatusResponse(

        dataset_id=dataset.id,

        status=dataset.status,

        rows=dataset.rows,

        columns=dataset.columns

    )