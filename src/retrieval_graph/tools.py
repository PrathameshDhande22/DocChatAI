from langchain_core.documents.base import Document
from langchain_core.vectorstores.base import VectorStore, VectorStoreRetriever
from langchain.tools import tool
from src.core.vectorstore import getVectorStore

# TODO: Later add the Filtering the Docs Based on Uploaded PDF based on the context


@tool(parse_docstring=True)
def retreive_docs(query: str) -> str:
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
            "k": 7,
            "fetch_k": 15,
            "lambda_mult": 0.8,
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
