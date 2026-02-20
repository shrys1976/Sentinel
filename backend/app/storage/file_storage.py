from pathlib import Path
import shutil
import uuid

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok = True)

def save_uploaded_file(file):

    dataset_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffic

    safe_filename = f"{dataset_id}{file_extension}"

    save_path = UPLOAD_DIR/safe_filename

    with save_path.open("wb") as buffer:

        shutil.copyfileobj(file.file,buffer)

        return dataset_id, str(save_path)