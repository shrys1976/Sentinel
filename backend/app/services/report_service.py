from sqlalchemy.orm import Session

from ..db.models import Dataset, Report
from .dataset_service import user_owns_dataset


def get_authorized_report(
    db: Session,
    dataset_id: str,
    user_id: str | None,
    session_id: str,
) -> tuple[Dataset | None, Report | None, str]:
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        return None, None, "not_found"

    if not user_owns_dataset(dataset, user_id, session_id):
        return None, None, "forbidden"

    report = (
        db.query(Report)
        .filter(Report.dataset_id == dataset_id)
        .order_by(Report.created_at.desc())
        .first()
    )
    return dataset, report, "ok"
