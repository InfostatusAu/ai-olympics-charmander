import os

def load_template(template_path: str) -> str:
    """Loads a markdown template from a specified file path."""
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()
