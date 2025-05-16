import os
import pickle
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


def load_vector_store(
        persist_path:str = "storage/faiss_index"
) -> FAISS:
    """
    Loads a FAISS vector store and its embedding model from disk.

    :param persist_path: Directory where the FAISS index and config are saved.
    :return: A FAISS vector store, ready for similarity search.
    """
    # Loading the embedded model if saved
    emb_file = os.path.join(persist_path,"config.")
    if os.path.exists(emb_file):
        # If you saved a config, load it; otherwise, reinstantiate directly
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    else:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store = FAISS.load_local(persist_path, embeddings)

    return vector_store