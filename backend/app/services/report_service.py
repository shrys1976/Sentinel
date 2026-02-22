from sqlalchemy.orm import Session

from ..db.models import Dataset, Report


def get_report_by_dataset_id(db: Session, dataset_id: str) -> tuple[Dataset | None, Report | None]:
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        return None, None

    report = (
        db.query(Report)
        .filter(Report.dataset_id == dataset_id)
        .order_by(Report.created_at.desc())
        .first()
    )
    return dataset, report
