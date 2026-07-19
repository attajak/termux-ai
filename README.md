# Termux-AI

[![Publish to PyPI](https://github.com/attajak/termux-ai/actions/workflows/release.yml/badge.svg)](https://github.com/attajak/termux-ai/actions/workflows/release.yml)

Termux-AI is a lightweight, zero-dependency CLI wrapper for AI models (Gemini, OpenAI, Groq, Mistral), built for Termux on Android and general Linux environments. It brings the power of LLMs directly to your command line, following the Unix philosophy of piping and standard streams.

## ⚡ Features
 * **🚀 Lightweight:** Uses standard Python requests. No heavy SDKs.
 * **🟢 Unix Compatible:** Supports piping (stdin).
 * **🛠 Configurable:** JSON configuration system (`ai -c`) for Prompts, Temperature, and Models.
 * **🛡 Secure:** Restricted file permissions (600) for configuration.
 * **⏳ Robust:** Built-in request timeouts and error handling.
 * **💬 Chat Mode:** Keeps conversation context using `--chat` flag.
 * **⚡ Streaming:** Real-time response streaming for a better experience.
 * **🔑 Env Support:** Supports `GEMINI_API_KEY`, `OPENAI_API_KEY`, `GROQ_API_KEY`, and `MISTRAL_API_KEY` environment variables.

## 📥 Installation
### Global Install (Recommended)
```bash
pip install termux-ai
# or
pipx install termux-ai
```

## 🔑 Setup
On the very first run, Termux-AI will ask for your AI provider and API Key.
*   Your configuration and history will be saved at `~/.local/share/termux-ai/`.

## 💻 Usage

### Basic Questions
```bash
ai "How do I untar a file in Linux?"
```

### Piping (The Power Move)
```bash
cat error.log | ai "Explain what caused this crash"
```

### Chat Mode (Contextual)
```bash
ai --chat "I want to learn Python."
# Next query...
ai --chat "What was the first thing I asked you?"
```

### ⚙️ Configuration
Run `ai -c` to open your configuration in your default editor.

## 🛠 Development
See [GEMINI.md](GEMINI.md) for development workflows, testing, and contribution guidelines.

## 📄 License
MIT License.
