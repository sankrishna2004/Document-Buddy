from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
load_dotenv()

embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def create_vectorstore(chunks: List[Document], save_path: str) -> Chroma:
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=save_path
    )

    # Persist to disk
    # vector_store.persist()
    return vector_store

def get_vectorstore(vector_path: str) -> Chroma:
    vector_store = Chroma(persist_directory=vector_path, embedding_function=embedding)
    return vector_store