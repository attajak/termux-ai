# Copilot Instructions for termux-ai

Purpose: guidance for Copilot sessions interacting with this repository.

Build & install
- Install runtime deps: pip install -r requirements.txt
- Install for development: python -m venv .venv && source .venv/bin/activate && pip install -e .
- Entry point (after install): ai → termai.cli:main

Tests & lint
- Dev dependencies listed in dev-requirements.txt: pytest, ruff, pre-commit, black, mypy.
- Install dev tools: pip install -r dev-requirements.txt
- Run full test suite: pytest
- Run a single test: pytest tests/test_providers.py::test_gemini_success -q
- Run linter: ruff check .
- Install pre-commit hooks: pre-commit install

High-level architecture
- CLI (termai/cli.py): parses args, reads stdin, handles flags (--config, --debug, --reinstall, --debug-config) and calls send_request.
- Config (termai/config.py): manages ~/.local/share/termai/config.json, first-run interactive setup, and migration from legacy key file. Editor priority: $EDITOR → vim → nano.
- Dispatcher (termai/api.py): selects provider by config["provider"] and forwards requests.
- Providers (termai/providers/): BaseProvider and concrete providers:
  - gemini.py: calls Google Generative Language endpoint; payload uses "generationConfig" and expects "candidates" with "content.parts".
  - openai.py: calls OpenAI chat completions endpoint; payload uses "messages" and standard "choices" response.
- UI & constants (termai/ui.py, termai/constants.py): colored CLI output and paths (DATA_DIR, CONFIG_FILE).

Key conventions and gotchas
- Config structure: top-level keys: provider, proxy, gemini_config, openai_config. Keep nested gemini_config and openai_config shapes when editing.
- Gemini generation config naming: fields like maxOutputTokens and generationConfig are used (notice camelCase for Gemini). OpenAI uses max_tokens and temperature (snake_case / typical OpenAI naming).
- Provider switching: change provider in config to "gemini" or "openai". The dispatcher instantiates providers from termai.providers.
- API keys: stored in ~/.local/share/termai/config.json. On first-run the CLI prompts for keys interactively; non-interactive runs require keys to already exist.
- Output format: default system_instruction asks providers to avoid Markdown/backticks/bolding — Copilot should respect that when crafting suggestions for user-facing text.
- Proxy: set top-level "proxy" in config to an HTTP(S) proxy URL; providers pass it to requests via proxies param.
- Exit codes: providers/cli return 0 on success, 1 on errors. Debug flags print raw responses when provided.
- No external SDKs: network calls use requests; keep changes minimal and avoid adding heavy dependencies without justification.

Files to inspect when changing behavior
- termai/config.py (config, migration, editor behavior)
- termai/cli.py (argument parsing and stdin handling)
- termai/providers/* (provider implementations and expected request/response shapes)
- pyproject.toml (entry-point script: ai)

Notes for Copilot sessions
- Prefer small, surgical edits. Preserve config migration logic and CLI flags.
- When suggesting code that affects CLI output, keep plain-text output expectations (no Markdown) and respect color constants.
- If introducing tests or linters, add their run instructions here and include a simple example for running an individual test.

License: MIT (see LICENSE)

---
If you'd like adjustments or want coverage added for other areas (packaging, CI, tests), say which area to expand.