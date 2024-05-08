from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = """Use the following context to answer the user's query. 
If you cannot answer the question, just respond with 'I don't know'.

Question:
{question}

Context:
{context}
"""

rag_prompt = ChatPromptTemplate.from_template(RAG_PROMPT)
