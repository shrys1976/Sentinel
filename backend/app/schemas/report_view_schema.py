from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ReportViewResponse(BaseModel):
    dataset: Dict[str, Any]
    sentinel_score: int
    top_issues: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    failed_analyzers: List[str] = Field(default_factory=list)
    sections: Dict[str, Any] = Field(default_factory=dict)
