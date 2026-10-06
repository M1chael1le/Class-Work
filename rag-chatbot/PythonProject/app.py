import os
import streamlit as st
from dotenv import load_dotenv
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()

DATA_DIR = "data/handbook"
API_KEY = os.getenv("GEMINI_API_KEY")

Settings.llm = GoogleGenAI(model="gemini-2.5-flash", api_key=API_KEY)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


@st.cache_resource
def get_query_engine():
    if not API_KEY:
        st.error("GEMINI_API_KEY not found. Add it to your .env file.")
        st.stop()
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()


st.title("Babson Handbook Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask about the student handbook"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the handbook..."):
            answer = get_query_engine().query(question).response
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})