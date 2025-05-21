
import os
import torch
from typing import List, Tuple

# LangChain utilities
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFacePipeline

# Transformers pipeline for local LLM
from transformers import pipeline

# Helper to load the FAISS index + embeddings
from vector_store import load_vector_store


def ask_question(
        query:str,
        vectorstore_dir: str = "storage/faiss_index",
        k:int = 3,
        model_name: str = "google/flan-t5-base",
        max_length: int = 256,
        temperature: float = 0.7
) -> Tuple[str,List[str]]:

    """
    1) Load the FAISS index with embeddings
    2) Retrieve the top-k most similar chunks for the query
    3) Generate an answer using a local Flan-T5 model
    4) Return the answer and the source chunk texts

    :param query: The user’s question text
    :param vectorstore_dir: Where FAISS index is saved
    :param k: Number of chunks to retrieve
    :param model_name: Hugging Face model for text generation
    :param max_length: Maximum tokens in generated answer
    :param temperature: Sampling temperature for LLM
    :return: (answer_str, [source_chunk1, source_chunk2, ...])
    """

    # ── Step 1: Load vector store (.faiss index + embeddings)
    vector_store = load_vector_store(persist_path=vectorstore_dir)

    # ── Step 2: Create a retriever for top-k similarity search
    retriever = vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs={"k":k}
    )

    # ── Step 3: Initialize a local text-generation pipeline
    #    We pick CPU or GPU based on availability
    device = 0 if torch.cuda.is_available() else -1

    hf_pipe = pipeline(
        task="text2text-generation",
        model=model_name,
        device=device,
        max_length=max_length,
        do_sample=True,
        temperature=temperature
    )
    llm = HuggingFacePipeline(pipeline=hf_pipe)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",         # combine all chunks into one prompt
        retriever=retriever,
        return_source_documents = True
    )

    result = qa_chain(query)
    answer = result["result"]
    sources = [doc.page_content for doc in result["source_documents"]]

    return answer, sources