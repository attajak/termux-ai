# termux-ai

A lightweight, zero-dependency CLI wrapper for Google's Gemini AI (and OpenAI), built for Termux and Linux environments.

## Project Overview

- **Purpose:** Provide a simple `ai` command to interact with LLMs directly from the terminal.
- **Key Features:** Supports stdin piping, configurable system prompts/models, and minimalist output.
- **Main Technologies:** Python 3.10+, `requests` library.
- **Architecture:** 
    - `termai/cli.py`: Entry point and argument parsing.
    - `termai/api.py`: Provider dispatcher.
    - `termai/config.py`: Configuration management (JSON-based).
    - `termai/providers/`: Modular AI provider implementations (Gemini, OpenAI).

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
    - Use `BaseProvider` for adding new AI services.
    - Prefer standard library or lightweight dependencies (e.g., `requests`) to keep the tool fast and portable.
    - CLI arguments are handled manually in `cli.py` to avoid heavy dependencies like `argparse` or `click` (though `argparse` is standard, the current implementation is manual).
- **Configuration:** 
    - Settings are stored in `~/.config/termux-ai/config.json` (or equivalent).
    - Sensible defaults are provided in `config.py`.
- **Testing:** New features should include tests in the `tests/` directory using `pytest`.
