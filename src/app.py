import asyncio
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from about import show_info
from core.embeddings import get_embedding_model
from ui.pdfload import processdocs
from utils import initialize_session

initialize_session()

# set the page layout
st.set_page_config("DocChat AI", ":books:")

# set the columns to divide the title and button
col1, col2 = st.columns([8, 1], vertical_alignment="center")
with col1:
    st.title("DocChat AI")
with col2:
    if st.button("❓"):
        show_info()


# variables to use globally
fileuploaded: list[UploadedFile] = []


# onclick
def onprocessclick(fileuploaded: list[UploadedFile]):
    st.session_state.processing = True
    asyncio.run(processdocs(fileuploaded))


# set the fileuploader in the sidebar
with st.sidebar:
    st.header("File Upload")
    st.markdown("Upload the `.pdf` files here to Get Started")

    # upload the files and store inmemory
    fileuploaded = st.file_uploader(
        "Upload PDF", type=["pdf"], help="Upload the PDFs", accept_multiple_files=True
    )

    if len(fileuploaded) > 0:
        st.button(
            "**Process**",
            help="Feed the Uploaded PDF to AI",
            type="primary",
            icon=":material/network_intelligence:",
            on_click=onprocessclick,
            args=(fileuploaded,),
            disabled=st.session_state.processing,
        )
