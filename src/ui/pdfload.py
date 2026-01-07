from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from streamlit.runtime.uploaded_file_manager import UploadedFile
import streamlit as st

from core.embeddings import get_embedding_model
from core.loaders import (
    load_and_split_pdfs,
    savefile_to_temp,
    split_documents,
)
from core.vectorstore import getVectorStore
from utils import add_Session, add_Session_Key, get_session_state


async def processdocs(docs: list[UploadedFile]):
    try:
        files_added: list[str] = get_session_state("files_added")

        # avoid processing the files for which it is already done
        files_to_process: list[UploadedFile] = [
            doc for doc in docs if doc.name not in files_added
        ]

        if len(files_to_process) > 0:
            st.toast("Processing Started", icon="spinner")

            temp_path: list[str] = savefile_to_temp(files_to_process)
            documents: list[Document] = await load_and_split_pdfs(temp_path)
            list_of_documents: list[Document] = split_documents(documents)

            # add the files to the session
            files_added.extend([filename.name for filename in files_to_process])
            add_Session({"files_added": files_added, "processing": False})

            await store_in_vector(list_of_documents, "pdfs")

        else:
            add_Session_Key("processing", False)
            st.toast("File Already Processed", icon=":material/done_outline:")
    except Exception as e:
        add_Session_Key("processing", False)
        st.toast("Error Occured During Loading the Docs", icon=":material/error:")
        print(e)


async def store_in_vector(documents: list[Document], collection_name: str):
    try:
        vectorStore: VectorStore = getVectorStore("Chroma", collection_name)

        await vectorStore.afrom_documents(documents, get_embedding_model())

    except Exception as e:
        print(e)
