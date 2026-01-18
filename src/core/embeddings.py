from langchain_huggingface import HuggingFaceEmbeddings
from langchain.embeddings.base import Embeddings
import streamlit as st


def get_embedding_model() -> Embeddings:
    return HuggingFaceEmbeddings(
        model_name="google/embeddinggemma-300m",
        model_kwargs={"device": "cuda"},
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )
