from pydantic import BaseModel
from typing import List, Optional
import uuid


class AnalysisArea(BaseModel):
    area: str
    issue: str
    suggestion: str
    show_simulation: bool = True


class AnalysisResult(BaseModel):
    id: str
    analysis_summary: Optional[str] = None
    areas: List[AnalysisArea] = []

    @classmethod
    def empty(cls) -> "AnalysisResult":
        return cls(
            id=str(uuid.uuid4()),
            analysis_summary="No areas detected.",
            areas=[]
        )

