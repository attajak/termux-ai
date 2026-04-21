import sys
from termai import cli

def test_help_returns_zero(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["ai", "--help"])
    assert cli.cli_entry_point() == 0
