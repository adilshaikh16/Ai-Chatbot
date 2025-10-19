import streamlit as st
import ollama

st.set_page_config(page_title="Adil's Offline AI", layout="wide")
st.title("🤖 Adil's Local AI (Offline)")

if "chat" not in st.session_state:
    st.session_state.chat = []

# Chat display
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Kuch puchhna hai?")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        full_response = ""

        response = ollama.chat(
            model="llama3",  # Model name (Llama3 recommended)
            messages=[{"role": "user", "content": user_input}]
        )

        full_response = response['message']['content']
        msg_placeholder.markdown(full_response)

    st.session_state.chat.append({"role": "assistant", "content": full_response})
