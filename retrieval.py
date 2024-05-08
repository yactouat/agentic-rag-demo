from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ArxivLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# loading a sample of RAG-related papers from arXiv
docs = ArxivLoader(query="Retrieval Augmented Generation", load_max_docs=5).load()

# chunking the documents into smaller pieces
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=350, chunk_overlap=50
)
chunked_documents = text_splitter.split_documents(docs)

# create embeddings then store them in our vector store
faiss_vectorstore = FAISS.from_documents(
    documents=chunked_documents,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
)
retriever = faiss_vectorstore.as_retriever()
