# building a RAG system about RAG !!
# building up on https://www.youtube.com/watch?v=SEA3eJrDc-k
import os
from dotenv import load_dotenv
from operator import itemgetter
from langchain_core.messages import HumanMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

# initializing the environment
load_dotenv()
os.environ["OPENAI_API_KEY"]

# using our simple RAG system
# from augmented import rag_prompt
# from generation import chat_model
# from retrieval import retriever
# retrieval_augmented_generation_chain = (
#         {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
#         | RunnablePassthrough.assign(context=itemgetter("context"))
#         | {"response": rag_prompt | chat_model, "context": itemgetter("context")}
# )
#
# response = retrieval_augmented_generation_chain.invoke({"question": "What is Retrieval Augmented Generation?"})
# print(response)

# using our graph agent
from graph import graph_app

inputs = {"messages": [
    HumanMessage(content="What is RAG in the context of Large Language Models? When did it break onto the scene?")]}
response = graph_app.invoke(inputs)
print(response)
