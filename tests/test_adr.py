from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from adr_agent_tools.adr import (
    ADR_INDEX_HEADER,
    calculate_next_adr_number,
    read_adr_template,
    setup_adr_directory,
)
from adr_agent_tools.mcp_server.server import adr, read_template


def test_setup_adr_directory_finds_git_root_and_initializes_index(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    nested = tmp_path / "src" / "pkg"
    nested.mkdir(parents=True)

    adr_dir = setup_adr_directory(nested)

    assert adr_dir == tmp_path / "docs" / "adr"
    assert adr_dir.is_dir()
    index_file = adr_dir / "README.md"
    assert index_file.is_file()
    assert index_file.read_text(encoding="utf-8") == ADR_INDEX_HEADER


def test_setup_adr_directory_preserves_existing_index(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    adr_dir = tmp_path / "docs" / "adr"
    adr_dir.mkdir(parents=True)
    index_file = adr_dir / "README.md"
    existing_content = "# Custom Index\n"
    index_file.write_text(existing_content, encoding="utf-8")

    result = setup_adr_directory(tmp_path)

    assert result == adr_dir
    assert index_file.read_text(encoding="utf-8") == existing_content


def test_setup_adr_directory_raises_without_git_root(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Git repository root not found"):
        setup_adr_directory(tmp_path)


def test_calculate_next_adr_number_empty_directory(tmp_path: Path) -> None:
    assert calculate_next_adr_number(tmp_path) == "0001"


def test_calculate_next_adr_number_existing_files(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Index", encoding="utf-8")
    (tmp_path / "0001-first-decision.md").write_text("# 0001", encoding="utf-8")
    (tmp_path / "0003-third-decision.md").write_text("# 0003", encoding="utf-8")
    (tmp_path / "notes.md").write_text("# Ignore me", encoding="utf-8")

    assert calculate_next_adr_number(tmp_path) == "0004"


def test_read_adr_template() -> None:
    template = read_adr_template()
    assert "## Context and Problem Statement" in template
    assert "## Decision Drivers" in template
    assert "## Considered Options" in template
    assert "## Confirmation & Verification Strategy" in template
    assert read_template() == template


def test_mcp_adr_tool(tmp_path: Path) -> None:
    import asyncio

    (tmp_path / ".git").mkdir()
    adr_dir = tmp_path / "docs" / "adr"
    adr_dir.mkdir(parents=True)
    (adr_dir / "0001-init.md").write_text("# 0001", encoding="utf-8")

    mock_resource = MagicMock()
    mock_resource.content = read_adr_template()
    ctx = MagicMock()
    ctx.read_resource = AsyncMock(return_value=[mock_resource])

    result = asyncio.run(adr(str(tmp_path), ctx))

    assert result.number_prefix == "0002"
    assert result.adr_directory == str(adr_dir)
    assert result.index_file == str(adr_dir / "README.md")
    assert "## Decision Outcome" in result.template
    assert len(result.guidelines) >= 5
