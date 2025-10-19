import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Adil AI", page_icon="🤖", layout="centered")

# Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.info("Built by Adil using OpenAI API")

# Title
st.title("🤖 Adil AI Chatbot")
st.caption("Your personal smart assistant — powered by OpenAI")

# Load API key securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = [
        {"role": "system", "content": "You are Adil AI, a friendly and intelligent assistant created by Adil."}
    ]

# Display previous messages
for msg in st.session_state.chat[1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    st.session_state.chat.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.chat
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # Save assistant reply
    st.session_state.chat.append({"role": "assistant", "content": reply})
