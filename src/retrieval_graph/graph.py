from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from src.retrieval_graph.edges import QUERY_OR_RESPOND, TOOLS
from src.retrieval_graph.tools import retreive_docs, uploaded_docs, current_datetime
from src.retrieval_graph.node import query_or_respond
from src.retrieval_graph.state import GraphState

builder = StateGraph(state_schema=GraphState)

builder.add_node(QUERY_OR_RESPOND, query_or_respond)
builder.add_node(TOOLS, ToolNode([retreive_docs, uploaded_docs, current_datetime]))

builder.add_edge(START, QUERY_OR_RESPOND)
builder.add_conditional_edges(QUERY_OR_RESPOND, tools_condition)
builder.add_edge(TOOLS, QUERY_OR_RESPOND)
builder.add_edge(QUERY_OR_RESPOND, END)

graph = builder.compile(name="RetrievalGraph")
