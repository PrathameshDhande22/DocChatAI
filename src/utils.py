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


SessionKeys = Literal["processing", "files_added", "messages", "provider"]


def initialize_session():
    defaults: SessionState = {
        "processing": False,
        "files_added": [],
        "messages": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_Session_Key(key: SessionKeys, value: Any) -> None:
    st.session_state[key] = value


def add_Session(session: dict[SessionKeys, Any]) -> None:
    for key, value in session.items():
        st.session_state[key] = value


def get_session_state(key: SessionKeys) -> Any:
    return st.session_state.get(key, None)


def convert_to_langchain_message(messages: list[chatmessagetuple]) -> list[BaseMessage]:
    return [
        HumanMessage(content=msg[1]) if msg[0] == "human" else AIMessage(content=msg[1])
        for msg in messages
        if msg[0] in ("human", "ai")
    ]
