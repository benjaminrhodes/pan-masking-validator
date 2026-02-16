"""Tests for CLI."""

from unittest.mock import patch
import sys

from src.cli import main


class TestCLI:
    """Tests for CLI main function."""

    def test_valid_pan(self):
        """Test CLI with valid PAN returns 0."""
        with patch.object(sys, "argv", ["pan-validate", "123456******1234"]):
            assert main() == 0

    def test_invalid_pan(self):
        """Test CLI with invalid PAN returns 1."""
        with patch.object(sys, "argv", ["pan-validate", "1234567890123456"]):
            assert main() == 1

    def test_no_arguments(self):
        """Test CLI with no arguments returns 1 and shows usage."""
        with patch.object(sys, "argv", ["pan-validate"]):
            assert main() == 1
