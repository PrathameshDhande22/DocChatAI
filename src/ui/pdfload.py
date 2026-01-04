from streamlit.runtime.uploaded_file_manager import UploadedFile
import streamlit as st

from core.loaders import (
    load_and_split_pdfs,
    savefile_to_temp,
    split_documents,
)


async def processdocs(docs: list[UploadedFile]):
    st.toast("Processing Started", icon="spinner")
    temp_path = savefile_to_temp(docs)
    documents = await load_and_split_pdfs(temp_path)
    print(documents)
    split_documents(documents)
