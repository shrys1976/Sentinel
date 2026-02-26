from fastapi import HTTPException
from .csv_ingestion import load_tolerant_csv

def extract_dataset_metadata(path: str):

    try:
        df, _ = load_tolerant_csv(path, nrows=5000)

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Unable to parse CSV."

        )


    # Count newline bytes to avoid platform text-decoding errors (e.g., cp1252 on Windows).
    with open(path, "rb") as f:
        rows = f.read().count(b"\n") - 1
    if rows < 0:
        rows = 0
    columns = len(df.columns)
    return rows, columns
