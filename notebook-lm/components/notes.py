import streamlit as st
import os

def show_notes():
    notes_path = "storage/notes"

    if not os.path.isdir(notes_path):
        os.makedirs(notes_path, exist_ok=True)
        st.write("No notes yet...")
        return

    files = os.listdir(notes_path)

    if not files:
        st.write("No notes saved yet...")
        return

    for file in files:
        with st.expander(file):
            with open(os.path.join(notes_path, file), "r", encoding="utf-8") as f:
                st.write(f.read())