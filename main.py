# building a RAG system about RAG !!
# building up on https://www.youtube.com/watch?v=SEA3eJrDc-k
from graphs import graph_app
from langchain_core.messages import HumanMessage


# using our graph agent
def use_graph_agent(inputs):
    response = graph_app.invoke(inputs)
    return response


inputs1 = {"messages": [
    HumanMessage(content="What is RAG in the context of Large Language Models? When did it break onto the scene?")]}
inputs2 = {"messages": [
    HumanMessage(content="Hey how you doing?")]}

print(use_graph_agent(inputs1))
print(use_graph_agent(inputs2))
