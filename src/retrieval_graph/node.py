from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.messages import SystemMessage, AIMessage

from src.retrieval_graph.state import GraphState
from src.core.llm_models import getLLMModel
from src.retrieval_graph.tools import retreive_docs
from src.retrieval_graph.prompt import query_or_respond as QueryPrompt

llm_model: BaseChatModel = getLLMModel("Google")


def query_or_respond(state: GraphState) -> GraphState:

    model_with_structured = llm_model.bind_tools(tools=[retreive_docs])

    prompt = ChatPromptTemplate.from_messages(
        messages=[
            SystemMessage(QueryPrompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    chain = prompt | model_with_structured

    airesponse: AIMessage = chain.invoke(input={"messages": state["messages"]})

    return {"messages": [airesponse]}

