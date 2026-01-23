from concurrent.futures import Future, ThreadPoolExecutor
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from streamlit.runtime.uploaded_file_manager import UploadedFile
import streamlit as st

from core.loaders import (
    load_and_split_pdfs,
    savefile_to_temp,
    split_documents,
)
from core.vectorstore import getVectorStore
from logger import get_logger
from ui.models.ProcessDocsResult import ProcessDocsResult
from utils import add_Session, add_Session_Key, get_session_state

logger = get_logger()


def docs_to_process(docs: list[UploadedFile]) -> list[UploadedFile]:
    files_added: list[str] = get_session_state("files_added")

    # avoid processing the files for which it is already done
    files_to_process: list[UploadedFile] = [
        doc for doc in docs if doc.name not in files_added
    ]
    if len(files_to_process) > 0:
        st.toast("Processing Started", icon="spinner")
        return files_to_process
    else:
        st.toast("File Already Processed", icon=":material/done_outline:")
        return []


def processdocs(docs: list[UploadedFile]) -> ProcessDocsResult:
    try:
        logger.info(
            "Starting PDF Processing for Files - "
            + ", ".join([doc.name for doc in docs])
        )
        temp_path: list[str] = savefile_to_temp(docs)
        documents: list[Document] = load_and_split_pdfs(
            temp_path, [doc.name for doc in docs]
        )
        list_of_documents: list[Document] = split_documents(documents)

        store_in_vector(list_of_documents, "pdfs")

        return ProcessDocsResult(
            files_added=[doc.name for doc in docs], processing=False, success=True
        )

    except Exception as e:
        logger.error(f"Error during PDF processing: {e}")
        logger.exception(e)
        return ProcessDocsResult(files_added=[], processing=False, success=False)


def store_in_vector(documents: list[Document], collection_name: str):
    try:
        logger.info("Storing Documents in Vector Store")
        vectorStore: VectorStore = getVectorStore("Chroma", collection_name)
        vectorStore.add_documents(documents)
    except Exception as e:
        logger.error(f"Error storing documents in vector store: {e}")
        logger.exception(e)


def handle_pdf_processing_executor(
    executor: ThreadPoolExecutor, fileuploaded: list[UploadedFile]
):
    list_docs_for_processing = docs_to_process(fileuploaded)
    if len(list_docs_for_processing) <= 0:
        logger.info("No New Documents to Process")
        add_Session_Key("processing",False)
        return
    future: Future[ProcessDocsResult] = executor.submit(
        processdocs, list_docs_for_processing
    )
    result: ProcessDocsResult = future.result()
    if future.done() and result.success:
        logger.info("PDF Processing Completed Successfully")
        existing_uploaded_files: list[str] = get_session_state("files_added")
        existing_uploaded_files.extend(result.files_added)
        add_Session(
            {
                "processing": result.processing,
                "files_added": existing_uploaded_files,
            }
        )
    elif future.cancelled() and future.exception():
        add_Session({"processing": False})
        logger.error(f"PDF Processing Cancelled: {future.exception()}")
        st.toast("Error Occured During Loading the Docs", icon=":material/error:")
    else:
        logger.error("PDF Processing Failed")
        add_Session({"processing": False})
        st.toast("Error Occured During Loading the Docs", icon=":material/error:")
