import os
from typing import List
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document



def ingest_document(chunks,persist_path: str = "storage/faiss_index"):
    """
    Converts document chunks into embeddings and stores them in a FAISS index.

    Args:
        chunks (list): List of document chunks to embed.
        persist_path (str): Directory to store the FAISS index.
    """

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # Wraps each chunk in a LangChain Document
    documents = [Document(page_content=chunk) for chunk in chunks]
    vector_store = FAISS.from_documents(documents,embeddings)
    os.makedirs(persist_path, exist_ok=True)
    vector_store.save_local(persist_path)
    print(f"✅ Ingested {len(chunks)} chunks and saved FAISS index to '{persist_path}'")
