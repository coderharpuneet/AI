from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    HumanMessage
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Mood AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

    .main {
        background-color: #0f172a;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 30px;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# TITLE
# ==========================================

st.markdown(
    '<div class="title">🤖 Mood AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Choose your AI personality and start chatting!</div>',
    unsafe_allow_html=True
)


# ==========================================
# GROQ MODEL
# ==========================================

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.9
)


# ==========================================
# AI MODES
# ==========================================

modes = {

    "😡 Angry Mode":
        "You are an angry AI agent. "
        "You respond aggressively and impatiently. "
        "Keep your responses entertaining but do not use hateful language.",

    "😂 Funny Mode":
        "You are a very funny AI agent. "
        "You respond with humor, jokes, sarcasm and playful comments.",

    "😢 Sad Mode":
        "You are a very sad AI agent. "
        "You respond in a depressed, emotional and melancholic tone."
}


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("🎭 Choose AI Mode")

    selected_mode = st.radio(
        "Select personality:",
        list(modes.keys())
    )

    st.divider()

    st.write("Current Mode:")

    st.info(selected_mode)

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = [
            SystemMessage(
                content=modes[selected_mode]
            )
        ]

        st.rerun()


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        SystemMessage(
            content=modes[selected_mode]
        )
    ]


# ==========================================
# CHANGE MODE
# ==========================================

if (
    st.session_state.messages[0].content
    != modes[selected_mode]
):

    st.session_state.messages = [
        SystemMessage(
            content=modes[selected_mode]
        )
    ]

    st.rerun()


# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):

        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):

        with st.chat_message("assistant"):
            st.markdown(message.content)


# ==========================================
# CHAT INPUT
# ==========================================

prompt = st.chat_input(
    "Type your message here..."
)


# ==========================================
# SEND MESSAGE
# ==========================================

if prompt:

    # Add user message
    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            response = model.invoke(
                st.session_state.messages
            )

            answer = response.content

            st.markdown(answer)

    # Save AI response
    st.session_state.messages.append(
        AIMessage(content=answer)
    )