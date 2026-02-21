import shutil
import uuid
from pathlib import Path

# Use path relative to backend root (works regardless of cwd when running uvicorn)
_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = _BACKEND_ROOT / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def save_uploaded_file(file):
    dataset_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    safe_filename = f"{dataset_id}{file_extension}"

    save_path = UPLOAD_DIR / safe_filename

    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return dataset_id, str(save_path)
