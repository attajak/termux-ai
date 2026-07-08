from pathlib import Path

# --- Configuration Paths ---
APP_NAME = "termux-ai"
DATA_DIR = Path.home() / ".local" / "share" / APP_NAME
# We now use a JSON file for all settings
CONFIG_FILE = DATA_DIR / "config.json"
# Legacy file path for migration
OLD_KEY_FILE = DATA_DIR / "key"
HISTORY_FILE = DATA_DIR / "history.json"

# --- Colors ---
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
