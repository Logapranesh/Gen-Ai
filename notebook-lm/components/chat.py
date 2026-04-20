import streamlit as st
from core.rag_chain import ask_rag
from utils.helpers import save_note
import datetime

def chat_ui():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask something about your PDF...")

    if user_input:
        # User message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        # 🔥 RAG response
        response = ask_rag(user_input)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.write(response)

        # Save note
        note_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_note(response, note_name)