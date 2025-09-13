import os
import asyncio

async def load_template(template_path: str) -> str:
    """Loads a markdown template from a specified file path."""
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")
    # Use asyncio.to_thread for file operations to avoid blocking the event loop
    return await asyncio.to_thread(lambda: open(template_path, "r", encoding="utf-8").read())

async def get_template(template_name: str) -> str:
    """Retrieves a template from the data/templates directory."""
    template_path = os.path.join("data", "templates", template_name)
    return await load_template(template_path)

