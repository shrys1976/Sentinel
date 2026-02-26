from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...core.dependencies import RequestContext, get_request_context
from ...db.session import get_db
from ...schemas.report_schema import ReportResponse
from ...schemas.report_view_schema import ReportViewResponse
from ...services.report_presenter import build_report_view
from ...services.plot_manager import list_plot_types
from ...services.report_service import get_authorized_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{dataset_id}", response_model=ReportResponse)
def fetch_report(
    dataset_id: str,
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
):
    dataset, report, status = get_authorized_report(
        db,
        dataset_id,
        context.user_id,
        context.session_id,
    )

    if status == "not_found":
        raise HTTPException(status_code=404, detail="Dataset not found")

    if status == "forbidden":
        raise HTTPException(status_code=403, detail="Access denied")

    if dataset.status in {"uploaded", "processing"}:
        return ReportResponse(dataset_id=dataset.id, score=0, report={}, status="processing")

    if dataset.status == "failed":
        raise HTTPException(status_code=500, detail="Analysis failed")

    if not report:
        return ReportResponse(dataset_id=dataset.id, score=0, report={}, status="processing")

    return ReportResponse(
        dataset_id=dataset.id,
        score=report.score,
        report=report.report_json,
        status="completed",
    )


@router.get("/{dataset_id}/view", response_model=ReportViewResponse)
def fetch_report_view(
    dataset_id: str,
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
):
    dataset, report, status = get_authorized_report(
        db,
        dataset_id,
        context.user_id,
        context.session_id,
    )

    if status == "not_found":
        raise HTTPException(status_code=404, detail="Dataset not found")

    if status == "forbidden":
        raise HTTPException(status_code=403, detail="Access denied")

    if dataset.status != "completed":
        raise HTTPException(status_code=400, detail="Analysis not completed")

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    available_plots = list_plot_types(db, dataset_id)
    view = build_report_view(report.report_json, report.score, dataset, available_plots)
    return view
