import os
import tempfile

def save_uploaded_file(uploaded_file) -> str:
    """Saves uploaded Streamlit files to temporary storage for local edge processing."""
    try:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        print(f"File handling error: {e}")
        return ""