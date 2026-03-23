"""Shared fixtures for Claude-MKII tests."""

import os
import tempfile

import pytest


@pytest.fixture
def tmp_dir():
    """Provide a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def sample_text_file(tmp_dir):
    """Create a simple text file and return its path."""
    path = os.path.join(tmp_dir, "sample.md")
    with open(path, "w") as f:
        f.write("# Title\n\nSome content here.\nAnother line.\n")
    return path
