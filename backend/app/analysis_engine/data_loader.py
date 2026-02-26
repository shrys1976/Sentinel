from app.utils.csv_ingestion import load_tolerant_csv

def load_dataframe(file_path: str):

    try :
        df, warnings = load_tolerant_csv(file_path)
        return df, warnings

    except Exception as e:

        raise RuntimeError(f"Dataset load failed: {e}")        

