from typing import Literal
from pydantic import BaseModel


class ProcessDocsResult(BaseModel):
    processing: bool
    files_added: list[str] | None
    success: bool
