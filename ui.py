import streamlit as st
import requests

API_URL = "http://54.242.78.94:8000/get_response"

st.set_page_config(page_title="Chatbot UI", page_icon="🤖")
st.title("🤖 Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.get(API_URL, params={"question": user_input})
                bot_reply = res.text  # FastAPI returns string
                st.markdown(bot_reply)
            except Exception as e:
                st.error(f"Error: {e}")
                bot_reply = "Error occurred"

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })