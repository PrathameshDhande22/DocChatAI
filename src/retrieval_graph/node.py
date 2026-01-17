from typing import Literal
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.messages import (
    SystemMessage,
    AIMessage,
    ToolMessage,
    HumanMessage,
    RemoveMessage,
    AnyMessage,
)
from langgraph.types import Command

from src.core.models.GradeDocument import GradeDocument
from src.retrieval_graph.state import GraphState
from src.core.llm_models import getLLMModel
from src.retrieval_graph.tools import current_datetime, retreive_docs, uploaded_docs
from src.retrieval_graph.edges import REWRITE_QUESTION, GENERATE_ANSWER
from src.retrieval_graph.prompt import (
    GENERATE_ANSWER_SYSTEM_PROMPT,
    GRADE_DOCUMENT_HUMAN,
    GRADE_DOCUMENT_PROMPT,
    QUERY_OR_RESPOND_PROMPT,
    REWRITE_QUESTION_HUMAN_PROMPT,
)

llm_model: BaseChatModel = getLLMModel("Google")


def query_or_respond(state: GraphState) -> GraphState:
    model_with_structured = llm_model.bind_tools(
        tools=[retreive_docs, current_datetime, uploaded_docs]
    )

    prompt = ChatPromptTemplate.from_messages(
        messages=[
            SystemMessage(QUERY_OR_RESPOND_PROMPT),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    chain = prompt | model_with_structured

    airesponse: AIMessage = chain.invoke(input={"messages": state["messages"]})

    return {"messages": [airesponse]}


def grade_documents(
    state: GraphState,
) -> Command[Literal["generate_answer", "rewrite_question"]]:
    llm_with_structured = llm_model.with_structured_output(GradeDocument)

    document: str | None = None
    question: str = ""

    if isinstance(state.get("messages")[-1], ToolMessage):
        document = state.get("messages")[-1].content
    if isinstance(state.get("messages")[-3], HumanMessage):
        question = state.get("messages")[-3].content

    if document is None or question is None:
        raise Exception("document and question is None")

    prompt = ChatPromptTemplate.from_messages(
        messages=[
            SystemMessage(GRADE_DOCUMENT_PROMPT),
            ("human", GRADE_DOCUMENT_HUMAN),
        ]
    )

    chain = prompt | llm_with_structured

    grade_document: GradeDocument = chain.invoke(
        input={"question": question, "document": document}
    )

    return (
        Command(goto=GENERATE_ANSWER, update={"improvement": None})
        if grade_document.score == "yes"
        else Command(
            goto=REWRITE_QUESTION, update={"improvement": grade_document.improvement}
        )
    )


def rewrite_question(state: GraphState) -> GraphState:
    prompt = ChatPromptTemplate.from_messages(
        messages=[("human", REWRITE_QUESTION_HUMAN_PROMPT)]
    )

    question: str = ""

    if isinstance(state.get("messages")[-3], HumanMessage):
        question = state.get("messages")[-3].content

    chain = prompt | llm_model

    airesponse = chain.invoke(
        {"question": question, "improvements": state.get("improvements", "")}
    )

    # Remove all the previous question to avoid the context rembering
    return {
        "messages": [
            RemoveMessage(id=message.id) for message in state.get("messages", [])[-3:]
        ]
        + [HumanMessage(content=airesponse.content)]
    }


def generate_answer(state: GraphState) -> GraphState:
    prompt = ChatPromptTemplate.from_messages(
        messages=[
            ("system", GENERATE_ANSWER_SYSTEM_PROMPT),
            ("human", GRADE_DOCUMENT_HUMAN),
        ]
    )

    document: str | None = None
    question: str = ""

    if isinstance(state.get("messages")[-1], ToolMessage):
        document = state.get("messages")[-1].content
    if isinstance(state.get("messages")[-3], HumanMessage):
        question = state.get("messages")[-3].content

    if document is None or question == "":
        raise Exception("document and question is None")

    print("documents=>", document, "Question:=>", question)

    chain = prompt | llm_model

    airesponse: AIMessage = chain.invoke(
        input={"question": question, "document": document}
    )

    return {"messages": [airesponse]}
