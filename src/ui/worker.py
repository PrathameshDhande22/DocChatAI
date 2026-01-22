import os
import streamlit as st
from concurrent.futures import ThreadPoolExecutor

from logger import get_logger

logger = get_logger()


@st.cache_resource
def get_executor() -> ThreadPoolExecutor:
    logger.info("Creating ThreadPoolExecutor for PDF Processing")
    return ThreadPoolExecutor(os.cpu_count() or 1)
