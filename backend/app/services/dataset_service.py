from sqlalchemy.orm import Session

from ..db.models import Dataset
from ..storage.file_storage import save_uploaded_file
from ..utils.dataframe_loader import extract_dataset_metadata


def create_dataset(
    db: Session,
    file,
    dataset_name: str,
    user_id=None,
    session_id=None,
):
    dataset_id, path = save_uploaded_file(file)

    rows, columns = extract_dataset_metadata(path)

    dataset = Dataset(
        id=dataset_id,
        name=dataset_name,
        file_path=path,
        user_id=user_id,
        session_id=session_id,
        rows=rows,
        columns=columns,
        status="uploaded",
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset


def get_datasets_for_user(
    db,
    user_id,
    session_id
):

    query = db.query(Dataset)

    if user_id :
        return query.filter(
            Dataset.user_id == user_id
        ).order_by(
            Dataset.created_at.desc()
        ).all()


    return query.filter(
        Dataset.session_id == session_id
    ).order_by(
        Dataset.created_at.desc()
    ).all()


def user_owns_dataset(

    dataset,
    user_id,
    session_id

):


    if user_id:
        return dataset.user_id == user_id


    return dataset.session_id == session_id


def get_dataset_status(


    db,
    dataset_id,
    user_id,
    session_id
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()


    if not dataset:
        return None, "not_found"

    if not user_owns_dataset(
        dataset,
        user_id,
        session_id        
    ):

         return None, "forbidden"

    return dataset, "ok"         
