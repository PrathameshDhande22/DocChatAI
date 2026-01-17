import os
from pathlib import Path
from chromadb import PersistentClient
from langchain_chroma import Chroma
from typing import Literal
from langchain_core.vectorstores import VectorStore
import streamlit as st
from core.embeddings import get_embedding_model


@st.cache_resource
def getVectorStore(
    provider: Literal["Chroma", "Pgvector"], collection_name: str
) -> VectorStore:
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
