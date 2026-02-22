from sqlalchemy.orm import Session

from ..analysis_engine.pipeline import run_analysis
from ..db.models import Dataset, Report
from ..db.session import SessionLocal


def process_dataset(dataset_id: str) -> None:
    db: Session = SessionLocal()
    dataset: Dataset | None = None

    try:
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            return

        dataset.status = "processing"
        db.commit()

        report_json, score = run_analysis(dataset.file_path)

        report = Report(
            dataset_id=dataset.id,
            report_json=report_json,
            score=score,
        )
        db.add(report)

        dataset.status = "completed"
        db.commit()
    except Exception as exc:
        if dataset is not None:
            dataset.status = "failed"
            db.commit()
        print(f"analysis worker failed for dataset {dataset_id}: {exc}")
    finally:
        db.close()
