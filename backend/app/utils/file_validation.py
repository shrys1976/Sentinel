from pathlib import Path

from fastapi import HTTPException, UploadFile

MAX_FILE_SIZE_MB = 100
ALLOWED_EXTENSIONS = {".csv"}


def validate_file_extension(file: UploadFile) -> None:
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only CSV files allowed")


def validate_file_size(file: UploadFile) -> None:
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large. Max size 100MB")


def validate_csv_structure(file: UploadFile) -> None:
    sample = file.file.read(4096)
    file.file.seek(0)

    if not sample:
        raise HTTPException(status_code=400, detail="CSV is empty")
