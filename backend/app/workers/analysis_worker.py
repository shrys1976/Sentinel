import logging

from sqlalchemy.orm import Session

from ..analysis_engine.pipeline import run_pipeline
from ..db.models import Dataset, Report
from ..db.session import SessionLocal
logger = logging.getLogger(__name__)


def process_dataset(dataset_id: str) -> None:
    db: Session = SessionLocal()
    dataset: Dataset | None = None

    try:
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            return

        dataset.status = "processing"
        db.commit()

        report_json, score = run_pipeline(dataset.file_path)

        report = Report(
            dataset_id=dataset.id,
            report_json=report_json,
            score=score,
        )
        db.add(report)

        dataset.status = "completed"
        db.commit()
    except Exception:
        db.rollback()
        if dataset is not None:
            try:
                dataset.status = "failed"
                db.commit()
            except Exception:
                db.rollback()
                logger.exception(
                    "failed to persist failed status for dataset_id=%s", dataset_id
                )
        logger.exception("analysis worker failed for dataset_id=%s", dataset_id)
    finally:
        db.close()
