from pathlib import Path
from uuid import uuid1
import streamlit as st

from core.exportpdf import create_pdf
from logger import get_logger
from utils import add_Session_Key, chatmessagetuple

logger = get_logger()

def export_chat_pdf(messages: list[chatmessagetuple]) -> None:
    """Export All the Chats from the "messages" session and save the PDF file path in the Session Key "file_path"

    Args:
        messages (list[chatmessagetuple]): List of Messages
    """
    try:
        output_path = str(
            Path.cwd().joinpath("exports").joinpath(str(uuid1()) + ".pdf")
        )
        exported_path = create_pdf(messages=messages, output_path=output_path)
        add_Session_Key("file_path", exported_path)
    except Exception as e:
        logger.error(f"Error exporting chat to PDF: {e}")
        logger.exception(e)
        st.error("Error Occurred while exporting chat to PDF")
