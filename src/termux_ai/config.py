import os
import sys
import json
import subprocess
import copy
import shutil
from .constants import APP_NAME, DATA_DIR, CONFIG_FILE, OLD_KEY_FILE

# --- Default Settings ---
DEFAULT_CONFIG = {
    "provider": "gemini",
    "proxy": "",
    "request_timeout": 30,
    "gemini_config": {
        "api_key": "",
        "model_name": "gemini-2.5-flash",
        "system_instruction": "You are a CLI assistant for command-line users. Do NOT use Markdown. Do NOT use backticks. Do NOT use bolding. Just write plain text. Keep answers concise.",
        "generation_config": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "maxOutputTokens": 1024,
        },
    },
    "openai_config": {
        "api_key": "",
        "model_name": "gpt-4o",
        "system_instruction": "You are a CLI assistant for command-line users. Do NOT use Markdown. Do NOT use backticks. Do NOT use bolding. Just write plain text. Keep answers concise.",
        "temperature": 0.7,
        "max_tokens": 1024,
    },
    "groq_config": {
        "api_key": "",
        "model_name": "llama-3.3-70b-versatile",
        "system_instruction": "You are a CLI assistant for command-line users. Do NOT use Markdown. Do NOT use backticks. Do NOT use bolding. Just write plain text. Keep answers concise.",
        "temperature": 0.7,
        "max_tokens": 1024,
    },
    "mistral_config": {
        "api_key": "",
        "model_name": "mistral-small-latest",
        "system_instruction": "You are a CLI assistant for command-line users. Do NOT use Markdown. Do NOT use backticks. Do NOT use bolding. Just write plain text. Keep answers concise.",
        "temperature": 0.7,
    },
}


def load_config():
    """
    Loads config.json.
    Handles migration from old path (~/.config/termai) to new path (~/.local/share/termux-ai),
    old 'key' file, and old flat config structure if needed.
    Creates default file if missing.
    """
    # 0. Migrate from old XDG config directory if it exists
    old_data_dir = Path.home() / ".config" / "termai"
    if old_data_dir.exists():
        print(f"[{APP_NAME}] Migrating data from {old_data_dir} to {DATA_DIR}...")
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        # Move files
        for item in old_data_dir.iterdir():
            shutil.move(str(item), str(DATA_DIR / item.name))
        old_data_dir.rmdir()
        print("Migration complete.")

    # Ensure directory exists with restricted permissions
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        os.chmod(DATA_DIR, 0o700)

    config = {}
    # 1. Check for Config File
    if CONFIG_FILE.exists():
        # Ensure file has restricted permissions
        if os.stat(CONFIG_FILE).st_mode & 0o077:
            os.chmod(CONFIG_FILE, 0o600)

        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print(f"[Error] Your config file ({CONFIG_FILE}) is invalid JSON.")
            print("Please fix it or delete it to reset defaults.")
            sys.exit(1)

        # Migration from old structure to new nested structure
        if "active_config" not in config:
            print(f"[{APP_NAME}] Migrating config to new simplified structure...")
            provider = config.get("provider", "gemini")
            new_config = {
                "provider": provider,
                "proxy": config.get("proxy", ""),
                "request_timeout": config.get("request_timeout", 30),
                "active_config": config.get(f"{provider}_config", DEFAULT_CONFIG.get(f"{provider}_config", {}))
            }
            # Create file with restricted permissions
            fd = os.open(CONFIG_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w") as f:
                json.dump(new_config, f, indent=4)
            print("Migration complete.")
            config = new_config

        # Check for environment variables and override active_config
        active_config = config.get("active_config", {})
        
        # Override based on provider
        provider = config.get("provider")
        env_key = os.getenv(f"{provider.upper()}_API_KEY")
        if env_key:
            active_config["api_key"] = env_key
            config["active_config"] = active_config

        return config

    # If no config file exists, proceed with first run setup
    # 2. Migration: If no config, check for old key file
    gemini_api_key = ""
    backup_file = DATA_DIR / "key.bak"
    if OLD_KEY_FILE.exists():
        print(f"[{APP_NAME}] Migrating legacy key file to new config format...")
        with open(OLD_KEY_FILE, "r") as f:
            gemini_api_key = f.read().strip()
        OLD_KEY_FILE.rename(backup_file)

    # 3. First Run Setup
    new_config = {
        "provider": "",
        "proxy": "",
        "request_timeout": 30,
        "active_config": {}
    }
    if sys.stdin.isatty():
        print(f"[{APP_NAME}] First run! Choose your primary AI provider.")
        provider = ""
        while provider not in ["1", "2", "3", "4"]:
            provider = input("Enter 1 for Gemini, 2 for OpenAI, 3 for Groq, 4 for Mistral: ").strip()

        provider_map = {"1": "gemini", "2": "openai", "3": "groq", "4": "mistral"}
        provider = provider_map[provider]
        
        new_config["provider"] = provider
        new_config["active_config"] = DEFAULT_CONFIG.get(f"{provider}_config", {})
        
        api_key = input(f"Enter your {provider.capitalize()} API Key: ").strip()
        if not api_key:
            print("Error: API key cannot be empty.")
            sys.exit(1)
        new_config["active_config"]["api_key"] = api_key
        
    else:
        # Default to Gemini if non-interactive and no config exists
        new_config["provider"] = "gemini"
        new_config["active_config"] = DEFAULT_CONFIG.get("gemini_config", {})
        
        if not gemini_api_key:
            return None  # Cannot proceed without an API key
        new_config["active_config"]["api_key"] = gemini_api_key

    # Save the new configuration with restricted permissions
    fd = os.open(CONFIG_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(new_config, f, indent=4)

    print(f"Configuration saved to {CONFIG_FILE}\n")

    # Clean up the legacy key backup file if it exists after migration
    if backup_file.exists():
        backup_file.unlink()

    return new_config


def open_editor():
    """
    Opens the config file in the user's preferred editor with a fallback mechanism.
    Priority: $EDITOR > vim > nano
    """
    # 1. Prioritize the user's explicit choice
    editor = os.getenv("EDITOR")

    # 2. If no $EDITOR, try to find 'vim'
    if not editor and shutil.which("vim"):
        editor = "vim"

    # 3. If still no editor, fall back to 'nano'
    if not editor:
        editor = "nano"

    print(f"Opening config in {editor}...")
    try:
        subprocess.call([editor, str(CONFIG_FILE)])
    except FileNotFoundError:
        print(
            f"[Error] Editor '{editor}' not found. Please install it or set the $EDITOR environment variable."
        )
        return 1
    return 0  # Return 0 for success
