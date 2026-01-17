from typing import Any, Literal, TypedDict
import streamlit as st

type chatmessagetuple = tuple[Literal["ai", "human"], str]


class SessionState(TypedDict):
    processing: bool
    files_added: list[str]
    messages: list[chatmessagetuple]


SessionKeys = Literal["processing", "files_added", "messages"]


def initialize_session():
    defaults: SessionState = {"processing": False, "files_added": [], "messages": []}
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
