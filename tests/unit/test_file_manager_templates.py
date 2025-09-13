import pytest
import os
from src.file_manager.templates import load_template

@pytest.fixture
def templates_dir(tmp_path):
    # Create a dummy templates directory within the temporary path
    template_path = tmp_path / "data" / "templates"
    template_path.mkdir(parents=True, exist_ok=True)
    
    # Create a dummy template file
    template_content = "# Test Template\nHello {{ name }}!"
    (template_path / "test_template.md").write_text(template_content)
    
    return template_path

async def test_load_template_success(templates_dir):
    template_name = "test_template.md"
    expected_content = "# Test Template\nHello {{ name }}!"
    loaded_content = await load_template(str(templates_dir / template_name))
    assert loaded_content == expected_content

async def test_load_template_not_found(templates_dir):
    template_name = "non_existent_template.md"
    with pytest.raises(FileNotFoundError):
        await load_template(str(templates_dir / template_name))