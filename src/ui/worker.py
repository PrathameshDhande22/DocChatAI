import streamlit as st
from concurrent.futures import ThreadPoolExecutor


@st.cache_resource
def get_executor() -> ThreadPoolExecutor:
    return ThreadPoolExecutor()
