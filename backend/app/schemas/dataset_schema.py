from pydantic import BaseModel
from typing import List


class DatasetUploadResponse(BaseModel):
    dataset_id: str
    rows: int
    columns: int
    status: str
    target_column: str|None


class DatasetHistoryItem(BaseModel):

    dataset_id : str
    name: str
    status: str
    rows: int|None
    columns: int|None
    target_column: str|None
    created_at : str


class DatasetHistoryResponse(BaseModel):

    datasets: List[DatasetHistoryItem]


class DatasetStatusResponse(BaseModel):
    dataset_id: str
    status: str
    rows: int|None
    columns : int | None
    target_column: str|None
