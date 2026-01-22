from typing import Any, Literal, TypedDict
import streamlit as st
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


from core.llm_models import Providers

type chatmessagetuple = tuple[Literal["ai", "human"], str]


class SessionState(TypedDict):
    processing: bool
    files_added: list[str]
    messages: list[chatmessagetuple]
    provider: Providers
    file_path: str


SessionKeys = Literal["processing", "files_added", "messages", "provider", "file_path"]


def initialize_session():
    """Initialize all the Session keys for the Streamlit application"""
    defaults: SessionState = {
        "processing": False,
        "files_added": [],
        "messages": [],
        "file_path": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_Session_Key(key: SessionKeys, value: Any) -> None:
    """Add the Specified Key with Value in the StreamLit Session

    Args:
        key (SessionKeys): Session Key to add
        value (Any): Value to add for the Session Key
    """
    st.session_state[key] = value


def add_Session(session: dict[SessionKeys, Any]) -> None:
    """Add multiple Session Keys with Values in the StreamLit Session

    Args:
        session (dict[SessionKeys, Any]): Dictionary of Session Keys and their Values
    """
    for key, value in session.items():
        st.session_state[key] = value


def get_session_state(key: SessionKeys) -> Any | None:
    """Get the Value for the Specified Key from the StreamLit Session

    Args:
        key (SessionKeys): Session Key to get the Value for

    Returns:
        Any | None: The value for the specified key, or None if the key does not exist.
    """
    return st.session_state.get(key, None)


def convert_to_langchain_message(messages: list[chatmessagetuple]) -> list[BaseMessage]:
    """Convert tuple of ("human",message) to Langchain Supported ChatMessage

    Args:
        messages (list[chatmessagetuple]): Tuple of ("human",message)

    Returns:
        list[BaseMessage]: List of the Langchain Message
    """
    return [
        HumanMessage(content=msg[1]) if msg[0] == "human" else AIMessage(content=msg[1])
        for msg in messages
        if msg[0] in ("human", "ai")
    ]
