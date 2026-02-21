from pydantic import BaseModel


class DatasetUploadResponse(BaseModel):
    dataset_id: str
    rows: int
    columns: int
    status: str
