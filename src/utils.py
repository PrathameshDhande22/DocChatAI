from typing import TypedDict
import streamlit as st


class SessionState(TypedDict):
    processing: bool


def initialize_session():
    defaults: SessionState = {"processing": False}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
