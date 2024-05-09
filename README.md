# agentic RAG demo

Building up on [this excellent video from AI Makerspace](https://www.youtube.com/watch?v=SEA3eJrDc-k), this project implements a RAG system that queries data about... RAG systems.

It uses a Streamlit UI to interact with the RAG system.

The LLMs under the hood are a mixture of ChatGPT 4 and 3.5.

## pre requisites

To be able to use the application, you need:

- an OpenAI API key

For the OpenAI API key, if it's not loaded from a `.env` file, the user will be prompted to enter it.

## run locally

To run the application locally: `streamlit run main.py` OR `python3 -m streamlit run main.py`.