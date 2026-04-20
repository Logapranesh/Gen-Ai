import streamlit as st
import os
from core.document_processor import process_pdf
from core.vector_store import add_documents

def sidebar():
    st.sidebar.header("📂 Upload Documents")

    os.makedirs("storage/uploads", exist_ok=True)

    uploaded_files = st.sidebar.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    selected_files = []

    if uploaded_files:
        for file in uploaded_files:
            file_path = os.path.join("storage/uploads", file.name)

            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

            chunks = process_pdf(file_path)

            add_documents(chunks)   # 🔥 Store in ChromaDB

            st.sidebar.success(f"{file.name} processed! Chunks: {len(chunks)}")

            selected_files.append(file.name)

    web_toggle = st.sidebar.checkbox("🌐 Enable Web Search")

    return selected_files, web_toggle