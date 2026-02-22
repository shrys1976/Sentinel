from sqlalchemy.orm import Session
from app.db.models import Dataset, Report
from app.services.dataset_service import (
    user_owns_dataset
)


def get_authorized_report(

    db: Session,
    dataset_id: str,
    user_id,
    session_id

):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()


    if not dataset:
        return None, None, "not_found"

    if not user_owns_dataset(

        dataset,
        user_id,
        session_id

    ):

        return None, None, "forbidden"

    report = db.query(Report).filter(
        Report.dataset_id == dataset_id

    ).first()
    return dataset, report, "ok"