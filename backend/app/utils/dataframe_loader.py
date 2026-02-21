import pandas as pd

def extract_dataset_metadata(path:str):

    df = pd.read_csv(path)
    rows,columns = df.shape
    return rows,columns