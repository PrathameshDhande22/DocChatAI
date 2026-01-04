from typing import Iterable
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.parsers import RapidOCRBlobParser
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
from streamlit.runtime.uploaded_file_manager import UploadedFile


async def load_and_split_pdfs(tempfile_path: list[str]) -> list[Document]:
    try:
        documents: list[Document] = []
        for file in tempfile_path:
            pdfloader = PyPDFLoader(
                file_path=file,
                images_parser=RapidOCRBlobParser(),
                mode="page",
                images_inner_format="markdown-img",
            )
            async for document in pdfloader.alazy_load():
                documents.append(document)
        return documents

    except Exception as e:
        print(e)
        return []


def split_documents(documents: Iterable[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    print(text_splitter.split_documents(documents))


def savefile_to_temp(docs: list[UploadedFile]) -> list[str]:
    """Saves the Uploaded file to the Temporary File

    Args:
        docs (list[UploadedFile]): List of Files Uploaded

    Returns:
        list[str]: List of temporary path
    """
    temp_path: list[str] = []
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        for file in docs:
            tmp.write(file.read())
            temp_path.append(tmp.name)
    return temp_path
