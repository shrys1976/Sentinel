from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ...analysis_engine.visualization_engine import PLOT_NAMES
from ...core.dependencies import RequestContext, get_request_context
from ...db.session import get_db
from ...services.plot_manager import ensure_single_plot_for_dataset, get_plot_image_bytes
from ...services.report_service import get_authorized_report

router = APIRouter(prefix="/plots", tags=["plots"])


@router.get("/{dataset_id}/{plot_type}")
def fetch_plot(
    dataset_id: str,
    plot_type: str,
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
):
    if plot_type not in PLOT_NAMES:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown plot '{plot_type}'. Allowed: {sorted(PLOT_NAMES)}",
        )

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
    if dataset.status != "completed" or not report:
        raise HTTPException(status_code=400, detail="Analysis not completed")

    image_bytes = get_plot_image_bytes(db, dataset_id, plot_type)
    if not image_bytes:
        try:
            image_bytes = ensure_single_plot_for_dataset(
                db=db,
                dataset_id=dataset_id,
                file_path=dataset.file_path,
                report_json=report.report_json if isinstance(report.report_json, dict) else {},
                target_column=dataset.target_column,
                plot_type=plot_type,
            )
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc))
        except Exception:
            raise HTTPException(status_code=500, detail="Plot regeneration failed")

    if not image_bytes:
        raise HTTPException(status_code=404, detail=f"Plot '{plot_type}' not found")

    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=86400"},
    )
