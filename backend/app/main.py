from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
# Import  RAG modules
from app.document_loader import load_document, chunk_text
from app.ingest import ingest_document
from app.rag_chain import ask_question


app = FastAPI(title="Smart Support Assistant API")

# Enabling CORS so  React frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "storage/uploads"
FAISS_DIR = "storage/faiss_index"
os.makedirs(UPLOAD_DIR,exist_ok=True)
os.makedirs(FAISS_DIR,exist_ok=True)

# Defining an API endpoint
# This function will handle HTTP POST requests made to the /upload URL.
# Used async to allow FastAPI to handle other requests while waiting for long-running requests
@app.post("/upload")
async def upload_doc(file: UploadFile=File(...)):
    """
    1) Receive an uploaded file
    2) Save it to disk
    3) Load, chunk, embed, and index it
    """
    # saving uploaded file
    file_path  = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open (file_path ,"wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to save file:{e}")

    # Loading full text from the saved document
    try:
        text = load_document(file_path)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    chunks = chunk_text(text)
    # Embeds and index the chunks in FAISS
    try:
        ingest_document(chunks, persist_path=FAISS_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    return {"status": "indexed", "filename": file.filename}


@app.post("/query")
async def query(payload:dict):
    """
    1) Receive a JSON body with a 'question' field
    2) Retrieve relevant chunks from FAISS
    3) Generate an answer using the local LLM
    4) Return the answer and the source chunks
    """
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="No 'question' provided in request body")
    try:
        answer, sources = ask_question(question, vectorstore_dir=FAISS_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

    return {
        "answer": answer,
        "sources": sources  # a list of chunk strings
    }