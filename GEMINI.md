# Termai: Modular Gemini & OpenAI CLI Wrapper

`termai` is a lightweight, zero-dependency (except for `requests`) Python CLI tool that provides a direct interface to Google Gemini and OpenAI models. Optimized for Termux on Android and general Linux environments, it follows the Unix philosophy of simple, composable tools that work with standard streams.

## Project Overview

- **Purpose:** Provide a fast, minimalist AI assistant in the terminal.
- **Main Technologies:** Python 3, `requests` library.
- **Architecture:** 
    - **Modular Package:** The project is structured as a standard Python package (`termai/`).
    - **Extensible Providers:** Uses a factory pattern in `api.py` to dynamically load models from `termai/providers/`.
    - **CLI Entry Point:** Managed via `pyproject.toml` and `termai/cli.py`.

## Key Features
- **Piping Support:** Handles `stdin` for seamless integration with shell commands (e.g., `cat log.txt | ai`).
- **Multi-Provider Support:** Currently supports Google Gemini (default) and OpenAI.
- **Configuration Management:**
    - Automatic first-time setup for API keys and provider selection.
    - Legacy migration from flat file formats to a nested JSON structure.
    - Built-in configuration editor (`ai --config`).
- **Debugging & Transparency:**
    - `--debug`: Shows raw API responses and internal states.
    - `--debug-config`: Prints active settings with redacted API keys.
- **Terminal Aesthetics:** Clean ANSI color-coded output.

## Building and Running

### Installation
The project is designed to be installed as a standard Python package:
```bash
# Global install (Recommended)
pip install .

# For development (Editable mode)
pip install -e .
```
This registers the global `ai` command.

### Commands
- **Basic Query:** `ai "your question"`
- **Piping:** `cat log.txt | ai "Explain this error"`
- **Module Run:** `python -m termai "query"`
- **Configuration:** `ai --config` (opens the JSON config in your default `$EDITOR`).
- **Reset/Reinstall:** `ai --reinstall` (wipes existing configuration and re-runs the first-time setup).
- **Debug API:** `ai --debug "query"`
- **Debug Config:** `ai --debug-config` (prints active settings with redacted API keys).

## Development Conventions

### Package Structure (`termai/`)
- `constants.py`: Centralized app constants, data paths, and ANSI colors.
- `config.py`: Configuration loading, legacy migration, and default settings.
- `ui.py`: Terminal output formatting, help menus, and CLI styling.
- `api.py`: Provider factory logic for request routing.
- `providers/`: Extensible directory for AI model implementations.
- `cli.py`: Main CLI execution flow and argument parsing.

### Adding New Providers
1. Create a new file in `termai/providers/` (e.g., `anthropic.py`).
2. Inherit from `BaseProvider` in `base.py`.
3. Register the new class in the `PROVIDERS` dictionary in `termai/api.py`.

### Default Configuration Schema
The application uses a nested JSON structure in `~/.local/share/termai/config.json`:
- `provider`: The active AI model provider (`gemini` or `openai`).
- `proxy`: Optional HTTP/HTTPS proxy.
- `gemini_config`: Configuration for Gemini (default: `gemini-2.5-flash`).
- `openai_config`: Configuration for OpenAI (default: `gpt-4o`).
- **System Instruction Defaults:** The default instruction for both providers is: *"You are a CLI assistant for command-line users. Do NOT use Markdown. Do NOT use backticks. Do NOT use bolding. Just write plain text. Keep answers concise."*

### Coding Style & Standards
- **Python Version:** Compatible with Python 3.x.
- **Dependencies:** Keep external dependencies to a minimum (currently only `requests`).
- **Error Handling:** Graceful handling of API quotas (429) and connection errors.
- **Security:** Never commit API keys or clear-text credentials; use the built-in migration and config tools.
