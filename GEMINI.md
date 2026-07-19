# Termux-AI - Project Instructions

Termux-AI is a lightweight, zero-dependency CLI wrapper for Google's Gemini AI and OpenAI, specifically designed for Termux on Android and general Linux environments. It adheres to the Unix philosophy, supporting standard input piping.

## Architecture & Design
- **Entry Point:** `src/termux_ai/cli.py`
- **Configuration:** Handled in `src/termux_ai/config.py` using `~/.config/termai/config.json`.
- **API Communication:** Managed via provider abstraction in `src/termux_ai/providers/`.
- **UI:** Simple console output, managed in `src/termux_ai/ui.py`.

## Development Workflows
- **Environment Setup:**
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  # For editable installs:
  pip install -e .
  ```
- **Running Tests:**
  ```bash
  pytest
  ```
- **Linting & Formatting (using Ruff):**
  ```bash
  # Check linting
  ruff check .
  # Format code
  ruff format .
  ```

## Conventions
- **Language:** Python 3.10+
- **Code Style:** Strictly enforce `ruff` configurations defined in `pyproject.toml`.
- **Testing:** All new features or bug fixes must be accompanied by a test case in the `tests/` directory.
- **Security:** Maintain strict file permissions (600) for sensitive configuration files (`config.json`).
