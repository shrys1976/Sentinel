import pandas as pd

def run_analysis(file_path:str):
    
    df = pd.read_csv(file_path)
    rows,columns = df.shape
    missing = df.isnull().mean().to_dict()

    report  = {

        "rows": rows,
        "columns": columns,
        "missing_ratio": missing
    }
    score = 80
    return report,score