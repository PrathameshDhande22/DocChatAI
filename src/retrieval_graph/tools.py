import datetime
from langchain_core.documents.base import Document
from langchain_core.vectorstores.base import VectorStore, VectorStoreRetriever
from langchain.tools import tool, ToolRuntime
from retrieval_graph.state import GraphState, ModelContext
from core.vectorstore import getVectorStore


@tool(parse_docstring=True)
def retreive_docs(query: str, runtime: ToolRuntime[ModelContext, GraphState]) -> str:
    """Retrieve Relevant Documents from the vector store based on a search query.

    Args:
        query (str): A short, focused search query representing the user's information need.

    Returns:
        str:  A single formatted string containing the retrieved document content.
    """
    store: VectorStore = getVectorStore("Chroma", "pdfs")
    retriever: VectorStoreRetriever = store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 10,
            "fetch_k": 20,
            "lambda_mult": 0.6,
            "filter": {"filename": {"$in": runtime.state["files_uploaded"]}},
        },
    )

    docs: list[Document] = retriever.invoke(query)
    return convert_doc_to_str(docs)


def convert_doc_to_str(docs: list[Document]) -> str:
    formatted_docs: list[str] = []
    for doc in docs:
        filename = doc.metadata.get("filename", "default.pdf")
        page_label = doc.metadata.get("page_label", 0)
        formmatted = f"""Source={filename} | Page:{page_label}
        {doc.page_content}
        """
        formatted_docs.append(formmatted)
    return "\n\n".join(formatted_docs)


@tool(description="Retreive the list of documents uploaded by the user")
def uploaded_docs(runtime: ToolRuntime[ModelContext, GraphState]) -> list[str]:
    """
    Retrieve the list of documents uploaded by the user.

    Returns:
        list[str]: A list of filenames representing the documents currently uploaded.
    """
    return runtime.state["files_uploaded"]


@tool(description="Returns the Current System Date and Time")
def current_datetime() -> str:
    """Returns the current system date and time.

    Returns:
        str: Current date and time in system default string format.
    """
    return datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
