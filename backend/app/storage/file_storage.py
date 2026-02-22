import uuid
import shutil
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = _BACKEND_ROOT / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)


def save_uploaded_file(file):

    dataset_id = str(uuid.uuid4())

    extension = Path(file.filename).suffix.lower()

    safe_filename = f"{dataset_id}{extension}"

    save_path = UPLOAD_DIR / safe_filename


    with save_path.open("wb") as buffer:

        shutil.copyfileobj(

            file.file,

            buffer,

            length=1024 * 1024

        )


    return dataset_id, str(save_path)




def delete_file(path: str):

    try:

        file_path = Path(path)
        if file_path.exists():
            file_path.unlink()

    except Exception as e:
        print("File delete failed:", e)   
