from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ArxivLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from operator import itemgetter

load_dotenv()

# RETRIEVAL
# loading a sample of RAG-related papers from arXiv
docs = ArxivLoader(query="Retrieval Augmented Generation", load_max_docs=5).load()

# chunking the documents into smaller pieces
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=350, chunk_overlap=50
)
chunked_documents = text_splitter.split_documents(docs)
# create embeddings then store them in our vector store,
# and create a retriever from the vector store
faiss_vectorstore = FAISS.from_documents(
    documents=chunked_documents,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
)
retriever = faiss_vectorstore.as_retriever()
# AUGMENTATION
rag_prompt_template = """Use the following context to answer the user's query. 
If you cannot answer the question, just respond with 'I don't know'.

Question:
{question}

Context:
{context}
"""
rag_prompt = ChatPromptTemplate.from_template(rag_prompt_template)
# GENERATION
chat_model = ChatOpenAI(model="gpt-3.5-turbo")
rag_chain = (
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | {"response": rag_prompt | chat_model, "context": itemgetter("context")}
)
