# building a RAG system about RAG !!
# building up on https://www.youtube.com/watch?v=SEA3eJrDc-k
import os
from dotenv import load_dotenv
from operator import itemgetter
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

# initializing the environment
load_dotenv()
os.environ["OPENAI_API_KEY"]

from augmented import rag_prompt
from generation import chat_model
from retrieval import retriever

retrieval_augmented_generation_chain = (
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | {"response": rag_prompt | chat_model, "context": itemgetter("context")}
)

response = retrieval_augmented_generation_chain.invoke({"question": "What is Retrieval Augmented Generation?"})
print(response)
