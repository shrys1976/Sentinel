from sqlalchemy.orm import Session

from app.db.models import Dataset
from app.storage.file_storage import save_uploaded_file
from app.utils.dataframe_loader import extract_dataset_metadata


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
