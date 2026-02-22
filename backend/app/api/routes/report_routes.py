from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...schemas.report_schema import ReportResponse
from ...services.report_service import get_report_by_dataset_id

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{dataset_id}", response_model=ReportResponse)
def fetch_report(dataset_id: str, db: Session = Depends(get_db)):
    dataset, report = get_report_by_dataset_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if dataset.status == "failed":
        raise HTTPException(status_code=500, detail="Analysis failed")

    if dataset.status in {"uploaded", "processing"}:
        return ReportResponse(dataset_id=dataset.id, score=0, report={}, status="processing")

    if not report:
        # Dataset may be completed but report write is not committed yet.
        return ReportResponse(dataset_id=dataset.id, score=0, report={}, status="processing")

    return ReportResponse(
        dataset_id=dataset.id, score=report.score, report=report.report_json, status="completed"
    )
