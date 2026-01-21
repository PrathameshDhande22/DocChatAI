from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from uuid import uuid1
import streamlit as st

from core.exportpdf import create_pdf
from utils import add_Session_Key, chatmessagetuple


def export_chat_pdf(messages: list[chatmessagetuple]):
    try:
        output_path = str(
            Path.cwd().joinpath("exports").joinpath(str(uuid1()) + ".pdf")
        )
        exported_path= create_pdf(messages=messages,output_path=output_path)
        add_Session_Key("file_path",exported_path)
    except Exception as e:
        print(e)
        st.error("Error Occurred while exporting chat to PDF")
