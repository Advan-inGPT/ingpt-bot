import requests
import streamlit as st
import requests

st.title("🧠 MAS - Chat bot")

if "chat" not in st.session_state:
    st.session_state.chat = []

API_URL = "http://localhost:8000/chat"  # Local FastAPI backend

def query_backend(prompt):
    try:
        res = requests.post(API_URL, json={"prompt": prompt}, timeout=60)
        return res.json().get("response", "⚠️ No response.")
    except Exception as e:
        return f"⚠️ Error: {e}"

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = query_backend(prompt)
    st.session_state.chat.append({"role": "assistant", "content": response})

for msg in st.session_state.chat:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

