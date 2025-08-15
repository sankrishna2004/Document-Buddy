from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import tempfile
from fastapi import File, UploadFile
from typing import List
from langchain_core.documents import Document

def get_docs(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(file_bytes)
        temp_path = temp.name

    try:
        loader = PyPDFLoader(temp_path)
        docs = loader.load()
    finally:
        os.remove(temp_path)

    document = "\n".join(doc.page_content for doc in docs)
    return document


def split_text(document: str) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([document])

    return chunks

