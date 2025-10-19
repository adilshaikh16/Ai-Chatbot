import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AdilGPT", layout="wide")
st.title("🤖 AdilGPT – Your Personal AI")

if "chat" not in st.session_state:
    st.session_state.chat = []

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712105.png", width=80)
    st.header("⚙️ Settings")
    system_prompt = st.text_area(
        "AI Personality:",
        "You are AdilGPT, a confident, friendly and slightly savage AI that replies in Roman Urdu unless told otherwise."
    )

# Display chat messages
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Apna message likho...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.chat
        )

        reply = response.choices[0].message.content
        msg_placeholder.markdown(reply)
        st.session_state.chat.append({"role": "assistant", "content": reply})
