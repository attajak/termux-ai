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
    "gemini_config": {
        "api_key": "",
        "model_name": "gemini-2.5-flash",
        "system_instruction": "You are a CLI assistant for command-line users. Do NOT use Markdown. Do NOT use backticks. Do NOT use bolding. Just write plain text. Keep answers concise.",
        "generation_config": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "maxOutputTokens": 1024
        }
    },
    "openai_config": {
        "api_key": "",
        "model_name": "gpt-4o",
        "system_instruction": "You are a CLI assistant for command-line users. Do NOT use Markdown. Do NOT use backticks. Do NOT use bolding. Just write plain text. Keep answers concise.",
        "temperature": 0.7,
        "max_tokens": 1024
    }
}

def load_config():
    """
    Loads config.json.
    Handles migration from old 'key' file and old flat config structure if needed.
    Creates default file if missing.
    """
    # Ensure directory exists
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    config = {}
    # 1. Check for Config File
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print(f"[Error] Your config file ({CONFIG_FILE}) is invalid JSON.")
            print("Please fix it or delete it to reset defaults.")
            sys.exit(1)

        # Migration from old flat structure to new nested structure
        if "api_key" in config:
            print(f"[{APP_NAME}] Migrating config to new nested structure...")
            new_config = copy.deepcopy(DEFAULT_CONFIG)
            # Preserve old top-level keys
            new_config["proxy"] = config.get("proxy", "")

            # Move gemini-specific keys
            new_config["gemini_config"]["api_key"] = config.get("api_key", "")
            new_config["gemini_config"]["model_name"] = config.get("model_name", DEFAULT_CONFIG["gemini_config"]["model_name"])
            new_config["gemini_config"]["system_instruction"] = config.get("system_instruction", DEFAULT_CONFIG["gemini_config"]["system_instruction"])
            new_config["gemini_config"]["generation_config"] = config.get("generation_config", DEFAULT_CONFIG["gemini_config"]["generation_config"])

            with open(CONFIG_FILE, "w") as f:
                json.dump(new_config, f, indent=4)
            print("Migration complete.")
            return new_config

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
    new_config = copy.deepcopy(DEFAULT_CONFIG)
    if sys.stdin.isatty():
        print(f"[{APP_NAME}] First run! Choose your primary AI provider.")
        provider = ""
        while provider not in ["1", "2"]:
            provider = input("Enter 1 for Gemini or 2 for OpenAI: ").strip()

        if provider == "1":
            new_config["provider"] = "gemini"
            if not gemini_api_key:
                print(f"[{APP_NAME}] Enter your Gemini API Key. Get it from aistudio.google.com")
                gemini_api_key = input("Gemini API Key: ").strip()
                if not gemini_api_key:
                    print("Error: Gemini key cannot be empty.")
                    sys.exit(1)
            new_config["gemini_config"]["api_key"] = gemini_api_key

        elif provider == "2":
            new_config["provider"] = "openai"
            print(f"[{APP_NAME}] Enter your OpenAI API Key. Get it from platform.openai.com")
            openai_api_key = input("OpenAI API Key: ").strip()
            if not openai_api_key:
                print("Error: OpenAI key cannot be empty.")
                sys.exit(1)
            new_config["openai_config"]["api_key"] = openai_api_key
    else:
        # Default to Gemini if non-interactive and no config exists
        # This part might need adjustment based on desired non-interactive behavior
        if not gemini_api_key:
             return None # Cannot proceed without an API key
        new_config["gemini_config"]["api_key"] = gemini_api_key

    # Save the new configuration
    with open(CONFIG_FILE, "w") as f:
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
        print(f"[Error] Editor '{editor}' not found. Please install it or set the $EDITOR environment variable.")
        return 1
    return 0 # Return 0 for success
