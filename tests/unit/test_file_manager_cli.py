import pytest
from click.testing import CliRunner
from src.file_manager.cli import cli

def test_create_dir_command(tmp_path):
    runner = CliRunner()
    new_dir = tmp_path / "test_cli_dir"
    result = runner.invoke(cli, ["create-dir", str(new_dir)])
    assert result.exit_code == 0
    assert f"Directory created: {new_dir}" in result.output
    assert new_dir.is_dir()

def test_create_dir_command_exists(tmp_path):
    runner = CliRunner()
    existing_dir = tmp_path / "existing_cli_dir"
    existing_dir.mkdir()
    result = runner.invoke(cli, ["create-dir", str(existing_dir)])
    assert result.exit_code == 0
    assert f"Directory already exists: {existing_dir}" in result.output
    assert existing_dir.is_dir()
