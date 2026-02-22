from pydantic import BaseModel
from typing import Dict, Any 

class ReportResponse(BaseModel):
    dataset_id :str
    score :  int
    report: Dict[str,Any]
    status:str