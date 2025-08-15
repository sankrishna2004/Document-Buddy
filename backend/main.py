from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessageChunk
import hashlib
import os
from backend.indexing import get_docs, split_text
from backend.chain import build_chain
from backend.vector import create_vectorstore

app = FastAPI()

@app.get("/")
def home():
    return {'message': 'PDF Question and Answer App'}

VECTOR_DB_DIR = "chroma_db"

def compute_file_hash(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()
@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    hash_id = compute_file_hash(file_bytes)
    vector_path = os.path.join(VECTOR_DB_DIR, hash_id)

    # If already exists, return the hash_id
    if os.path.exists(vector_path):
        return JSONResponse(content={"message": "File already exists", "pdf_id": hash_id}, status_code=200)

    document = get_docs(file_bytes)
    chunks =split_text(document)
    vector_store = create_vectorstore(chunks,save_path = vector_path)
    return JSONResponse(content={"message" : "successfully uploaded", "pdf_id" : hash_id}, status_code=200)

@app.post('/query')
def query(question: str = Form(...),hash_id: str = Form(...)):
    vector_path = os.path.join(VECTOR_DB_DIR, hash_id)
    chain = build_chain(vector_path)

    def generate():
        for chunk in chain.stream(question):
            if isinstance(chunk, AIMessageChunk):
                yield chunk.content
            else:
                yield str(chunk)

    return StreamingResponse(generate(), media_type='text/plain')