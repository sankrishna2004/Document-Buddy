from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import load_prompt
from langchain_chroma import Chroma
from backend.vector import embedding, get_vectorstore
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

def build_chain(vector_path):
    vector_store = get_vectorstore(vector_path)

    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    prompt = load_prompt("template.json")

    llm = ChatOllama(
        model="llama3:8b",
        temperature=1.0
    )

    parser = StrOutputParser()

    def context_docs(retrieved_docs: List[Document]) -> str:
        context = "\n".join(doc.page_content for doc in retrieved_docs)
        return context

    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(context_docs),
        'question': RunnablePassthrough()
    })

    main_chain = parallel_chain | prompt | llm | parser
    return main_chain