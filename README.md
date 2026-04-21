# Termux-AI

[![Release](https://github.com/attajak/termux-ai/actions/workflows/release.yml/badge.svg)](https://github.com/attajak/termux-ai/actions/workflows/release.yml)

Termux-Ai is a lightweight, zero-dependency CLI wrapper for Google's Gemini AI, built for Termux on Android and general Linux environments.
It brings the power of Large Language Models (LLMs) directly to your command line, following the Unix philosophy of piping and standard streams.

## ⚡ Features
 * **🚀 Lightweight:** Uses standard Python requests. No heavy SDKs or complex dependencies.
 * **🟢 Unix Compatible:** Supports piping (stdin). Feed logs, code, or text files directly into the AI.
 * **🛠 Configurable:** Built-in JSON configuration system (ai --config) to edit System Prompts, Temperature, and Models.
 * **⚡ Fast:** Defaults to gemini-2.5-flash for instant responses.
 * **🎨 Clean UI:** Minimalist output with syntax-highlighted green text.
 * **🧹 Auto-Cleanup:** The installer sets everything up and deletes the repository to save space.

## 📥 Installation
### Method 1: Global Install (Recommended)
You can install TermuxAI directly using `pip` or `pipx`:
```bash
# Using pip
pip install termux-ai
# Using pipx (isolated environment)
pipx install termux-ai
```
This will make the `ai` command available globally.

### Method 2: Manual Setup (for Development)
If you want to contribute or run Termai in a development environment:
```bash
git clone https://github.com/attajak/termux-ai.git
cd termux-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
**or**
```bash
pip install -e git+https://github.com/attajak/termux-ai.git
```

## 🔑 Setup
On the very first run, Termai will ask for your Google Gemini API Key.
 * Get a free API key here: Google AI Studio
 * Run the command:
 ```bash
   ai "hello"
   ```

 * Paste your key when prompted. It will be saved locally.
## 💻 Usage
1. Basic Questions
Ask anything directly from the terminal.
ai "How do I untar a file in Linux?"

2. Piping (The Power Move)
Feed output from other commands into Termux-AI.
Debug an error log:
```bash
cat error.log | ai "Explain what caused this crash"
```

Explain a script:
```bash
cat install.sh | ai "What does this script do?"
```

Generate code and save it:
```bash
ai "Write a Python hello world script" > hello.py
```

## ⚙️ Configuration
Termux-AI comes with a built-in configuration editor. You can change the AI provider, model, and personality.
Run:
```bash
ai --config
```

This opens `config.json` in your preferred editor. The editor is chosen based on the following priority:
1.  The `$EDITOR` environment variable.
2.  `vim` (if installed).
3.  `nano` (as a fallback).

The configuration file looks like this:
```json
{
    "provider": "gemini",
    "proxy": "http://user:pass@127.0.0.1:1080",
    "gemini_config": {
        "api_key": "YOUR_GEMINI_KEY",
        "model_name": "gemini-2.5-flash",
        "system_instruction": "You are a CLI assistant for Termux...",
        "generation_config": {
            "temperature": 0.7,
            "maxOutputTokens": 1024
        }
    },
    "openai_config": {
        "api_key": "YOUR_OPENAI_KEY",
        "model_name": "gpt-4o",
        "system_instruction": "You are a helpful assistant.",
        "temperature": 0.7,
        "max_tokens": 1024
    }
}
```

*   **`provider`**: Set to `"gemini"` or `"openai"` to choose your AI provider.
*   **`proxy`**: (Optional) Set an HTTP or HTTPS proxy for all requests.
*   **`gemini_config`**: Settings for when `provider` is `"gemini"`.
    *   `model_name`: Change to `gemini-2.5-pro` or other available models.
    *   `system_instruction`: Give the AI a persona.
    *   `temperature`: Set to `1.0` for creative answers, `0.1` for precise logic.
*   **`openai_config`**: Settings for when `provider` is `"openai"`.
    *   `model_name`: Change to `gpt-3.5-turbo`, etc.
    *   `system_instruction`: A different persona for ChatGPT.
    *   `temperature`: Controls randomness.
    *   `max_tokens`: The maximum number of tokens to generate.
## 🛠 Development
If you want to contribute or run Termai in a development environment:

1.  **Clone and set up a virtual environment:**
    ```bash
    git clone https://github.com/attajak/termux-ai.git
    cd termux-ai
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install runtime dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install development tools (linters & test runner):**
    ```bash
    pip install -r dev-requirements.txt
    ```

4.  **Install editable package for development:**
    ```bash
    pip install -e .
    # 'ai' will use the local development version
    ```

Testing & linting

- Run all tests:
```bash
pytest
```

- Run a single test:
```bash
pytest tests/test_providers.py::test_gemini_success -q
```

- Run the linter (ruff):
```bash
ruff check .
```

- Install pre-commit hooks:
```bash
pre-commit install
```

## ❓ Help & Troubleshooting
**Command List:**
```bash
ai --help
```

**Re-configure API Keys:**

To reset and re-enter your API keys, use the `--reinstall` flag.
```bash
ai --reinstall
```

**Debug Mode:**

If the AI isn't responding or you are getting errors, run:
```bash
ai --debug "your question"
```
This will print the raw server response and error codes.

**Debug Configuration:**
If you are having issues with your configuration, you can use the `--debug-config` flag to print the loaded configuration. API keys will be redacted for security.
```bash
ai --debug-config
```

## 🗑 Uninstallation
### If installed via pip/pipx:
```bash
pip uninstall termux-ai
# or
pipx uninstall termux-ai
```

## 📄 License
This project is licensed under the MIT License.
You are free to use, modify, and distribute this software. See the LICENSE file for more details.
<p align="center">
Made with ❤️ for CLI enthusiasts
</p>

---

<details>
<summary>Source codes</summary>
https://github.com/estiaksoyeb/termai.git
</details>
