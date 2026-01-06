from typing import Any, Literal, TypedDict
import streamlit as st


class SessionState(TypedDict):
    processing: bool
    files_added: list[str]


SessionKeys = Literal["processing", "files_added"]


def initialize_session():
    defaults: SessionState = {"processing": False, "files_added": []}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_Session_Key(key: SessionKeys, value: Any) -> None:
    st.session_state[key] = value


def add_Session(session: dict[SessionKeys, Any]) -> None:
    for key, value in session.items():
        st.session_state[key] = value


def get_session_state(key: SessionKeys) -> Any:
    return st.session_state.get(key, "")
