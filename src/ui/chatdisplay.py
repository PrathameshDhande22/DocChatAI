import streamlit as st
from langchain.messages import AIMessageChunk
from langchain_core.callbacks import UsageMetadataCallbackHandler

from logger import get_logger
from retrieval_graph.edges import REWRITE_QUESTION
from retrieval_graph.graph import graph
from utils import (
    add_Session_Key,
    convert_to_langchain_message,
    get_session_state,
    chatmessagetuple,
)

logger = get_logger()


def add_message_to_session(message: chatmessagetuple) -> None:
    """Add the Message to the Streamlit Session to the key "messages"

    Args:
        message (chatmessagetuple): Chat Message Tuple in the form of ("human",message) or ("ai",message)
    """
    messages: list[chatmessagetuple] = get_session_state("messages")
    messages.append(message)
    add_Session_Key("messages", messages)


def display_chat_box(message: chatmessagetuple) -> None:
    """Display the Streamlit Chat Message box for "ai" or "human" message

    Args:
        message (chatmessagetuple): Chat Message Tuple in the form of ("human",message) or ("ai",message)
    """
    add_message_to_session(message)
    chat_message_box = st.chat_message(message[0])
    chat_message_box.markdown(message[1])


def display_ai_chat_box() -> None:
    """Display the AI Chat Message box by invoking the Langgraph Graph / Workflow"""
    logger.info("Invoking the Graph for AI Response")
    try:
        usagehandler = UsageMetadataCallbackHandler()

        with st.chat_message("ai"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Processing..."):
                for chunk in graph.stream(
                    input={
                        "files_uploaded": get_session_state("files_added"),
                        "rewritten": 0,
                        "messages": convert_to_langchain_message(
                            get_session_state("messages")
                        ),
                    },
                    context={"provider": get_session_state("provider")},
                    stream_mode=["custom", "messages"],
                    print_mode=["custom", "debug"],
                    config={
                        "callbacks": [
                            usagehandler,
                        ]
                    },
                ):
                    if chunk[0] == "messages":
                        if (
                            isinstance(chunk[1][0], AIMessageChunk)
                            and chunk[1][1]["langgraph_node"] != REWRITE_QUESTION
                        ):
                            full_response += chunk[1][0].content
                            message_placeholder.markdown(full_response.strip())
            add_message_to_session(("ai", full_response))
            logger.info(f"Token Usage: {usagehandler.usage_metadata} tokens used")
    except Exception as e:
        st.error("Some Error Occured while Invoking the Graph / Workflow")
        logger.error(f"Error in Graph Invocation: {e}")
        logger.exception(e)
        message_placeholder.markdown("Sorry, something went wrong.")