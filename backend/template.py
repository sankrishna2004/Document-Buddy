from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
        You are an AI assistant.
        Give answers to the questions from given context.
        If context is insufficient, respond with "I don't know."

        {context}

        Question: {question}
        """,
    input_variables=["context", "question"]
)

prompt.save('template.json')