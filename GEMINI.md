# termux-ai

A lightweight, zero-dependency CLI wrapper for Google's Gemini AI (and OpenAI), built for Termux and Linux environments.

## Project Overview

- **Purpose:** Provide a simple `ai` command to interact with LLMs directly from the terminal.
- **Key Features:** Supports stdin piping, configurable system prompts/models, and minimalist output.
- **Main Technologies:** Python 3.10+, `requests` library.
- **Architecture:** 
    - `termai/cli.py`: Entry point using `argparse` for robust argument handling.
    - `termai/api.py`: Provider dispatcher with a lazy-loading registry.
    - `termai/config.py`: Configuration management with restricted file permissions (600).
    - `termai/providers/`: Modular AI provider implementations (Gemini, OpenAI) extending `BaseProvider`.

## Building and Running

### Setup for Development
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install the package in editable mode
pip install -e .
```

### Running Tests and Linting
```bash
# Run all tests
pytest

# Run linter
ruff check .

# Format code
ruff format .
```

### Basic Usage
```bash
# Direct question
ai "How do I untar a file in Linux?"

# Piping input
cat log.txt | ai "Explain this error"

# Configuration
ai --config
```

## Development Conventions

- **Language:** Python 3.10+.
- **Style:** Adheres to Ruff's default rules (line length 88, double quotes).
- **Architecture Patterns:** 
    - **Provider Registry:** New providers should be registered in `termai/api.py` to be lazily loaded.
    - **BaseProvider Helpers:** Utilize `_get_common_params`, `_handle_debug`, and `_safe_json_decode` for shared logic across providers.
    - **Security First:** API keys must be sent via HTTP headers (e.g., `x-goog-api-key`) rather than URL parameters.
    - **Stability:** All network requests must include a `timeout` and handle `json.JSONDecodeError`.
- **Configuration:** 
    - Settings are stored in `~/.config/termai/config.json`.
    - Includes a `request_timeout` setting (default 30s) and nested provider configs.
- **Testing:** New features should include tests in the `tests/` directory using `pytest`. Mock all network calls.
