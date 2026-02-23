import pandas as pd

def load_dataframe(file_path: str):

    try :
        df = pd.read_csv( file_path, low_memory=True)
        return df

    except Exception as e:

        raise RuntimeError(f"Dataset load failed: {e}")        

