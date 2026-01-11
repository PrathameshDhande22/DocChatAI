from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from src.retrieval_graph.edges import (
    GENERATE_ANSWER,
    GRADE_DOCUMENTS,
    QUERY_OR_RESPOND,
    REWRITE_QUESTION,
    TOOLS,
)
from src.retrieval_graph.tools import retreive_docs, uploaded_docs, current_datetime
from src.retrieval_graph.node import (
    generate_answer,
    grade_documents,
    query_or_respond,
    rewrite_question,
)
from src.retrieval_graph.state import GraphState

builder = StateGraph(state_schema=GraphState)

builder.add_node(QUERY_OR_RESPOND, query_or_respond)
builder.add_node(TOOLS, ToolNode([retreive_docs, uploaded_docs, current_datetime]))
builder.add_node(GRADE_DOCUMENTS, grade_documents)
builder.add_node(REWRITE_QUESTION, rewrite_question)
builder.add_node(GENERATE_ANSWER, generate_answer)

builder.add_edge(START, QUERY_OR_RESPOND)
builder.add_conditional_edges(QUERY_OR_RESPOND, tools_condition)
builder.add_edge(TOOLS, GRADE_DOCUMENTS)
builder.add_edge(REWRITE_QUESTION, QUERY_OR_RESPOND)
builder.add_edge(GENERATE_ANSWER, END)

graph = builder.compile(name="RetrievalGraph")
