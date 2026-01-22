from langchain_huggingface import HuggingFaceEmbeddings
from langchain.embeddings.base import Embeddings


def get_embedding_model() -> Embeddings:
    """Embedding Models to USE with Cuda Support

    Returns:
        Embeddings: Model
    """
    return HuggingFaceEmbeddings(
        model_name="google/embeddinggemma-300m",
        model_kwargs={"device": "cuda"},
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )
