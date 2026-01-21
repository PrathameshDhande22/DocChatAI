from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from about import show_info
from ui.chatdisplay import display_ai_chat_box, display_chat_box
from ui.exporter import export_chat_pdf
from ui.pdfload import handle_pdf_processing_executor
from ui.worker import get_executor
from utils import add_Session, get_session_state, initialize_session

initialize_session()
load_dotenv()
executor: ThreadPoolExecutor = get_executor()

# set the page layout
st.set_page_config(
    "DocChat AI",
    ":books:",
    menu_items={"about": "", "Get Help": "https://github.com/prathameshdhande22"},
)

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


@st.fragment
def exportchat_pdf_fragment():
    container = st.container()

    file_path: str = st.session_state.get("file_path")

    if file_path is None or len(file_path) <= 0:
        with container:
            st.button(
                "Export as PDF",
                type="secondary",
                use_container_width=True,
                help="Export all your chats as PDF",
                icon=":material/file_export:",
                disabled=len(get_session_state("messages")) <= 0,
                on_click=export_chat_pdf,
                args=(get_session_state("messages"),),
            )
    else:
        with container:
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    icon=":material/download:",
                    data=f,
                    file_name="chats.pdf",
                    mime="application/pdf",
                    type="secondary",
                    use_container_width=True,
                )


# set the fileuploader in the sidebar
with st.sidebar:
    if st.button(
        "New Chat",
        help="New Chat with New Model",
        type="secondary",
        icon=":material/chat:",
        width="stretch",
    ):
        add_Session({"messages": [], "provider": "Qwen 3", "file_path": ""})

    exportchat_pdf_fragment()
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

    display_ai_chat_box()
    st.rerun()
