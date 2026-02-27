from __future__ import annotations

from sqlalchemy.orm import Session

from ..analysis_engine.visualization_engine import PLOT_NAMES, generate_all_plot_bytes
from ..db.models import AnalysisPlot


def upsert_plots_for_dataset(
    db: Session,
    dataset_id: str,
    file_path: str,
    report_json: dict,
    target_column: str | None,
) -> list[str]:
    existing = {
        row.plot_type
        for row in db.query(AnalysisPlot.plot_type).filter(AnalysisPlot.dataset_id == dataset_id).all()
    }
    missing_plot_types = sorted(PLOT_NAMES - existing)
    if not missing_plot_types:
        return sorted(existing)

    generated = generate_all_plot_bytes(
        file_path=file_path,
        report=report_json,
        target_column=target_column,
        requested_plot_names=set(missing_plot_types),
    )

    for plot_type, image_bytes in generated.items():
        db.add(
            AnalysisPlot(
                dataset_id=dataset_id,
                plot_type=plot_type,
                image_data=image_bytes,
            )
        )

    db.flush()
    all_plot_types = {
        row.plot_type
        for row in db.query(AnalysisPlot.plot_type).filter(AnalysisPlot.dataset_id == dataset_id).all()
    }
    return sorted(all_plot_types)


def get_plot_image_bytes(db: Session, dataset_id: str, plot_type: str) -> bytes | None:
    row = (
        db.query(AnalysisPlot)
        .filter(
            AnalysisPlot.dataset_id == dataset_id,
            AnalysisPlot.plot_type == plot_type,
        )
        .first()
    )
    if not row:
        return None
    return bytes(row.image_data)


def list_plot_types(db: Session, dataset_id: str) -> list[str]:
    return sorted(
        row.plot_type
        for row in db.query(AnalysisPlot.plot_type).filter(AnalysisPlot.dataset_id == dataset_id).all()
    )


def ensure_single_plot_for_dataset(
    db: Session,
    dataset_id: str,
    file_path: str,
    report_json: dict,
    target_column: str | None,
    plot_type: str,
) -> bytes | None:
    existing = get_plot_image_bytes(db, dataset_id, plot_type)
    if existing:
        return existing

    if plot_type not in PLOT_NAMES:
        return None

    generated = generate_all_plot_bytes(
        file_path=file_path,
        report=report_json,
        target_column=target_column,
        requested_plot_names={plot_type},
    )
    payload = generated.get(plot_type)
    if not payload:
        return None

    db.add(
        AnalysisPlot(
            dataset_id=dataset_id,
            plot_type=plot_type,
            image_data=payload,
        )
    )
    db.commit()
    return payload
