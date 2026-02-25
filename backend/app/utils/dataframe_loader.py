import pandas as pd
from fastapi import HTTPException

def extract_dataset_metadata(path: str):

    try:

        df = pd.read_csv(

            path,
            nrows=5000,
            low_memory=True,
            encoding_errors="replace",

        )

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

