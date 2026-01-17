import streamlit as st

from utils import add_Session_Key, get_session_state, chatmessagetuple


def display_chat_box(message: chatmessagetuple):
    messages: list[chatmessagetuple] = get_session_state("messages")
    messages.append(message)
    add_Session_Key("messages", messages)
    chat_message_box = st.chat_message(message[0])
    chat_message_box.markdown(message[1])


def display_ai_chat_box(message: chatmessagetuple):
    with st.chat_message("ai"):
        st.status("Searching in Docs")
