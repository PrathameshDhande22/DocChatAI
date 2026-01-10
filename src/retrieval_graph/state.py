from langgraph.graph import MessagesState


class GraphState(MessagesState):
    files_uploaded: list[str]
