import os
from typing import List
import fitz
import docx
from langchain.text_splitter import  RecursiveCharacterTextSplitter



def load_document(filepath:str) -> str:
    """
    Load the full text of a document from disk.
    Supports .txt, .pdf, and .docx based on file extension.
    """

    print(f"load_document received filepath: {filepath} (type: {type(filepath)})")
    ext = os.path.splitext(filepath)[1].lower()
    print(f"Extracted extension before lower(): {ext} (type: {type(ext)})")

    if ext == ".txt":
        # Simple text file: reading and returning all contents
        with open(filepath,"r",encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        # PDF: using PyMuDF to extract text from each page
        text = []
        with fitz.open(filepath) as pdf:
            for page in pdf:
                text.append(page.get_text())
        return "\n".join(text)
    elif ext == ".docx":
        # DOCX: using python-docx to extract text from each paragraph
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def chunk_text(
        text: str,
        chunk_size:int = 1000,
        overlap: int = 200,
) -> List[str]:
    """
    Split a long text into overlapping chunks.

    :param text: The full document text
    :param chunk_size: Maximum characters per chunk
    :param overlap: Characters of overlap between adjacent chunks
    :return: List of text chunks
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, #Target Size per chunk
        chunk_overlap=overlap, # overlap to preserve context
        length_function=len # measure length by character count
    )
    return splitter.split_text(text)