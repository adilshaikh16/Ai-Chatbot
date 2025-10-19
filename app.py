import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Get API Key
api_key = os.getenv("OPENAI_API_KEY")

# Error handle if key missing
if not api_key:
    st.error("❌ OPENAI_API_KEY not found. Add it in .env or Streamlit Secrets.")
    st.stop()

# Initialize client
client = OpenAI(api_key=api_key)

# Streamlit page setup
st.set_page_config(page_title="AdilGPT", layout="wide")
st.title("🤖 AdilGPT – Online ChatGPT Clone")

# Chat memory
if "chat" not in st.session_state:
    st.session_state.chat = []

# Sidebar – AI Personality
with st.sidebar:
    st.header("⚙️ Settings")
    system_prompt = st.text_area(
        "AI Personality (System Message):",
        "You are AdilGPT, a confident, street-smart and friendly AI who replies in Roman Urdu with attitude."
    )

# Display previous chat
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Kuch puchhna hai?")

if user_input:
    # Show user message
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI Response
    with st.chat_message("assistant"):
        msg_box = st.empty()
        msg_box.markdown("⏳ Thinking...")

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.chat
            )
            ai_reply = response.choices[0].message.content
            msg_box.markdown(ai_reply)
            st.session_state.chat.append({"role": "assistant", "content": ai_reply})

        except Exception as e:
            msg_box.error(f"⚠️ Error: {str(e)}")
