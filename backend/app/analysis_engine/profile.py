import pandas as pd

def build_dataset_profile(
    df: pd.DataFrame
):

    numeric_columns  = df.select_dtypes(include = "number").columns.tolist()
    categorical_columns = df.select_dtypes(exclude="number").columns.tolist()

    profile = {

        "rows": len(df),
        "columns": len(df.columns),
        "numeric_columns" : numeric_columns,
        "categorical_columns" : categorical_columns,
        "column_names": df.columns.tolist()
    }

    return profile
