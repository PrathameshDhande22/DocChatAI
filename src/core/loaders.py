from typing import Iterable
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.parsers import RapidOCRBlobParser
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
from streamlit.runtime.uploaded_file_manager import UploadedFile
from logger import get_logger

logger = get_logger()


def load_and_split_pdfs(
    tempfile_path: list[str], filename: list[str]
) -> list[Document]:
    """Load the Uploaded Document and Split the PDF with OCR Support

    Args:
        tempfile_path (list[str]): Document or PDF saved in temp path
        filename (list[str]): Original Filename

    Returns:
        list[Document]: List of Document for the provided tempfile_path.
    """
    try:
        logger.info(
            "Loading PDFs with OCR support for Filenames: " + ", ".join(filename)
        )
        documents: list[Document] = []
        for tempfile, originalfile in list(zip(tempfile_path, filename)):
            pdfloader = PyPDFLoader(
                file_path=tempfile,
                images_parser=RapidOCRBlobParser(),
                mode="page",
                images_inner_format="text",
            )
            for document in pdfloader.lazy_load():
                document.metadata["filename"] = originalfile
                documents.append(document)
        return documents

    except Exception as e:
        logger.warning("OCR Loading failed, falling back to non-OCR loading method.")
        return _load_and_split_pdfs_wot_ocr(tempfile_path, filename)


def _load_and_split_pdfs_wot_ocr(
    tempfile_path: list[str], filename: list[str]
) -> list[Document]:
    """Load the Uploaded Document and Split the PDF without OCR Support

    Args:
        tempfile_path (list[str]): Document or PDF saved in temp path
        filename (list[str]): Original Filename

    Raises:
        e: EXCEPTION if loading fails

    Returns:
        list[Document]: List of Document for the provided tempfile_path.
    """

    try:
        logger.info("Loading PDFs without OCR for Filenames: " + ", ".join(filename))
        documents: list[Document] = []
        for tempfile, originalfile in list(zip(tempfile_path, filename)):
            pdfloader = PyPDFLoader(file_path=tempfile, mode="page")
            for document in pdfloader.lazy_load():
                document.metadata["filename"] = originalfile
                documents.append(document)
        return documents
    except Exception as e:
        logger.error(f"Error loading PDFs without OCR: {e}")
        raise e


def split_documents(documents: Iterable[Document]) -> list[Document]:
    logger.info("Splitting Documents into smaller chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    return text_splitter.split_documents(documents)


def savefile_to_temp(docs: list[UploadedFile]) -> list[str]:
    """Saves the Uploaded file to the Temporary File Path

    Args:
        docs (list[UploadedFile]): List of Files Uploaded

    Returns:
        list[str]: List of temporary path
    """
    temp_path: list[str] = []
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        for file in docs:
            logger.info("Saving file to temporary path: " + file.name)
            tmp.write(file.read())
            temp_path.append(tmp.name)
            logger.info("File saved to temporary path: " + tmp.name)
    return temp_path
