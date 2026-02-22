from pathlib import Path
import uuid
import shutil


UPLOAD_DIR = Path("uploads")

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