import os
from pathlib import Path
from chromadb import PersistentClient
from langchain_chroma import Chroma
from typing import Literal
from langchain_core.vectorstores import VectorStore
import streamlit as st
from core.embeddings import get_embedding_model


def getVectorStore(
    provider: Literal["Chroma", "Pgvector"], collection_name: str
) -> VectorStore:
    """Get the Vector Store for the Specified Provider

    Args:
        provider (Literal[&quot;Chroma&quot;, &quot;Pgvector&quot;]): Provider of which to instantiate the vector store.
        collection_name (str): Collection name to store the embedding

    Raises:
        Exception: Vector Store is not implemented for the Provided Provider

    Returns:
        VectorStore: Langchain Base Class for VectorStore
    """
    match provider:
        case "Chroma":
            client = PersistentClient(path=Path.cwd().joinpath("store"))
            return Chroma(
                collection_name=collection_name,
                embedding_function=get_embedding_model(),
                client=client,
            )
        case _:
            raise Exception("Implement other Provider Store")
