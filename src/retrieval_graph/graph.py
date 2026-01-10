from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from src.retrieval_graph.node import query_or_respond
from src.retrieval_graph.state import GraphState

builder = StateGraph(state_schema=GraphState)

builder.add_node("query_or_respond", query_or_respond)

builder.add_edge(START, "query_or_respond")
builder.add_edge("query_or_respond", END)

graph = builder.compile(name="RetrievalGraph")
