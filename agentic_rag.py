# building a RAG system about RAG !!
# building up on https://www.youtube.com/watch?v=SEA3eJrDc-k
from graphs import get_graph_app
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
import streamlit as st


# using our graph agent
def generate_graph_agent_response(inputs, openai_api_key: str | None = None):
    response = get_graph_app().invoke(inputs)
    return response


def validate_openai_api_key(api_key: str | None) -> bool:
    if api_key is None:
        return False
    return api_key.startswith("sk-")


load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

st.title('🔗 meta RAG 🔗')
st.subheader("answer questions about RAG")
st.write('this is my first shot at both Streamlit and at RAG apps!')
st.write('you can help me improve by providing feedback at https://github.com/yactouat/agentic-rag-demo/discussions')

with st.form('rag_form'):
    query = st.text_area('Ask me anything about RAG')
    submitted = st.form_submit_button('RAG me up!')

    if submitted and not validate_openai_api_key(openai_api_key):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    elif submitted:
        formatted_inputs = {"messages": [HumanMessage(content=query)]}
        res = generate_graph_agent_response(formatted_inputs, openai_api_key)
        output = res["messages"][-1].content if not isinstance(res["messages"][-1], str) else res["messages"][-1]
        st.info(output)
