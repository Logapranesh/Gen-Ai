import streamlit as st
from components.sidebar import sidebar
from components.chat import chat_ui
from components.notes import show_notes

st.set_page_config(layout="wide")

st.title("📘 NotebookLM Replica")

# Sidebar
uploaded_files, web_toggle = sidebar()

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat")
    chat_ui()

with col2:
    st.header("📝 Notes")
    show_notes()