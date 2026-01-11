from typing import Literal, Optional
from pydantic import BaseModel, Field


class GradeDocument(BaseModel):
    score: Literal["yes", "no"] = Field(description="", examples=["yes"])
    improvement: Optional[str] = Field(default=None, description="Improvement need")
