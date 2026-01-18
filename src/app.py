from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from about import show_info
from ui.chatdisplay import display_ai_chat_box, display_chat_box
from ui.pdfload import handle_pdf_processing_executor
from ui.worker import get_executor
from utils import get_session_state, initialize_session

initialize_session()
load_dotenv()
executor: ThreadPoolExecutor = get_executor()

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
    handle_pdf_processing_executor(executor, fileuploaded)


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


provider = st.selectbox(
    accept_new_options=False,
    label="Select Provider",
    options=["Gemini 2.5 Flash", "Qwen 3", "Mistral Large 3", "GPT OSS 120b"],
    key="provider",
    help="Select the Chat Message Provider",
    index=1,
    disabled=len(get_session_state("messages")) > 0,
)


# Display the previous messages
for message in get_session_state("messages"):
    chat_message_box = st.chat_message(message[0])
    chat_message_box.markdown(message[1])

# Chat Input Message
if input_message := st.chat_input(
    placeholder="Ask Your DocChatAI!",
    accept_file=False,
    max_chars=150,
):
    display_chat_box(("human", input_message))

    display_ai_chat_box(input_message)
