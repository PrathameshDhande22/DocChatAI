from typing import Literal, TypedDict
from langgraph.graph import MessagesState

from core.llm_models import Providers


class GraphState(MessagesState):
    files_uploaded: list[str] = []
    improvement: str | None = None
    rewritten: int = 0


class ModelContext(TypedDict):
    provider: Providers = "Qwen 3"
