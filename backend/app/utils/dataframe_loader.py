import pandas as pd
from fastapi import HTTPException

def extract_dataset_metadata(path:str):

    try:

        df = pd.read_csv(

            path,
            nrows=5000,
            low_memory=True

        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Unable to parse CSV."

        )


    rows = sum(1 for _ in open(path)) - 1
    columns = len(df.columns)
    return rows, columns


