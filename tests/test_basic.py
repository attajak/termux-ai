import sys
from termux_ai import cli


def test_help_returns_zero(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["ai", "--help"])
    # Mock print_help to avoid actual printing during tests if desired,
    # but cli_entry_point should return the result of print_help()
    monkeypatch.setattr("termux_ai.ui.print_help", lambda: 0)
    assert cli.cli_entry_point() == 0


def test_debug_config_redaction(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["ai", "--debug-config"])

    fake_config = {
        "provider": "gemini",
        "gemini_config": {"api_key": "secret_key_1234"},
        "openai_config": {"api_key": "secret_key_5678"},
    }
    monkeypatch.setattr("termux_ai.cli.load_config", lambda: fake_config)

    ret = cli.cli_entry_point()
    assert ret == 0
    captured = capsys.readouterr()
    assert "***1234" in captured.out
    assert "***5678" in captured.out
    assert "secret_key" not in captured.out


def test_prompt_parsing(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["ai", "hello", "world"])
    monkeypatch.setattr("termux_ai.cli.load_config", lambda: {"provider": "gemini"})

    # Mock stdin to behave like a terminal (no piping)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)

    called_with = []

    def mock_send_request(config, user_input, debug, **kwargs):
        called_with.append(user_input)
        return 0

    monkeypatch.setattr("termux_ai.cli.send_request", mock_send_request)
    cli.cli_entry_point()
    assert "hello world" in called_with


def test_piping_input(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["ai"])
    monkeypatch.setattr("termux_ai.cli.load_config", lambda: {"provider": "gemini"})

    # Mock stdin to behave like a pipe
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    monkeypatch.setattr(sys.stdin, "read", lambda: "piped content")

    called_with = []

    def mock_send_request(config, user_input, debug, **kwargs):
        called_with.append(user_input)
        return 0

    monkeypatch.setattr("termux_ai.cli.send_request", mock_send_request)
    cli.cli_entry_point()
    assert "piped content" in called_with


def test_reinstall_logic(monkeypatch, tmp_path):
    # Mock CONFIG_FILE path
    test_config = tmp_path / "config.json"
    test_config.write_text("{}")
    monkeypatch.setattr("termux_ai.cli.CONFIG_FILE", test_config)

    monkeypatch.setattr(sys, "argv", ["ai", "--reinstall"])
    # Mock load_config to avoid interactive setup
    monkeypatch.setattr("termux_ai.cli.load_config", lambda: {})

    cli.cli_entry_point()
    assert not test_config.exists()
