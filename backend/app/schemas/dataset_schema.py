from pydantic import BaseModel
from typing import List


class DatasetUploadResponse(BaseModel):
    dataset_id: str
    rows: int
    columns: int
    status: str


class DatasetHistoryItem(BaseModel):

    dataset_id : str
    name: str
    status: str
    rows: int|None
    columns: int|None
    created_at : str


class DatasetHistoryResponse(BaseModel):

    datasets: List[DatasetHistoryItem]    