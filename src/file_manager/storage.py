import os

def create_directory(path: str):
    """Creates a directory if it does not exist."""
    os.makedirs(path, exist_ok=True)

def save_markdown_file(file_path: str, content: str):
    """Saves markdown content to a specified file."""
    create_directory(os.path.dirname(file_path))
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def read_markdown_file(file_path: str) -> str:
    """Reads markdown content from a specified file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def file_exists(file_path: str) -> bool:
    """Checks if a file exists."""
    return os.path.exists(file_path)
