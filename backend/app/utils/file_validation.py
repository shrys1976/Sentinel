from fastapi import UploadFile, HTTPException
import csv
from pathlib import Path


MAX_FILE_SIZE_MB = 100
ALLOWED_EXTENSIONS = {".csv"}

def validate_file_extension(file:UploadFile):

    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="only CSV files allowed "
        )

def validate_file_size(file: UploadFile):

    file.file.seek(0,2)
    size=file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code = 413,
            detial = "File too large. Max size 100MB"
        )    

def valudate_csv_structure(file: UploadFile):

    try:
        sample = file.file.read(4096)
        file.file.seek(0)
        sample.decode("utf-8")
        csv.Sniffer().sniff(sample.decode("utf-8"))

    except Exception :
        raise HTTPException(
            status_code = 400,
            detail = "Invalid CSV format."
        )        