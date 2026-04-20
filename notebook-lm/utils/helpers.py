import os

def save_note(content, filename):
    os.makedirs("storage/notes", exist_ok=True)

    path = f"storage/notes/{filename}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)