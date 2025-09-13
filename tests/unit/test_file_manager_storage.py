import pytest
import os
from src.file_manager.storage import save_markdown_file, read_markdown_file, file_exists, create_directory

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

def test_save_markdown_file(temp_dir):
    file_path = os.path.join(temp_dir, "test_prospect.md")
    content = "# Test Prospect\n\nThis is a test markdown file."
    save_markdown_file(file_path, content)
    assert os.path.exists(file_path)
    with open(file_path, "r") as f:
        assert f.read() == content

def test_read_markdown_file(temp_dir):
    file_path = os.path.join(temp_dir, "read_test.md")
    content = "## Read Test\n\nContent to be read."
    with open(file_path, "w") as f:
        f.write(content)
    
    read_content = read_markdown_file(file_path)
    assert read_content == content

def test_file_exists(temp_dir):
    file_path = os.path.join(temp_dir, "existing_file.md")
    with open(file_path, "w") as f:
        f.write("exists")
    
    assert file_exists(file_path)
    assert not file_exists(os.path.join(temp_dir, "non_existing_file.md"))

def test_create_directory(temp_dir):
    new_dir_path = os.path.join(temp_dir, "new_dir", "sub_dir")
    create_directory(new_dir_path)
    assert os.path.isdir(new_dir_path)
