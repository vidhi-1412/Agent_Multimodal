import streamlit as st
from main import run
import time

# Page setup
st.set_page_config(
    page_title="Agentic AI System",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS (🔥 makes UI modern)
st.markdown("""
<style>
.chat-bubble {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.user {
    background-color: #DCF8C6;
    text-align: right;
}
.bot {
    background-color: #F1F0F0;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 Agentic AI Manufacturing Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    industry = st.selectbox(
        "Industry",
        ["Aluminum", "Steel", "Electronics"]
    )
    location = st.text_input("Location", "India")

# Chat input
user_input = st.chat_input("Ask something...")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# When user sends message
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Agents thinking..."):
            time.sleep(1)
            response = run()

        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})