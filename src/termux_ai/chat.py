import json
from .constants import HISTORY_FILE


def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def add_to_history(role, content):
    history = load_history()
    history.append({"role": role, "content": content})
    # Keep only the last 10 turns (20 messages) to prevent huge files
    if len(history) > 20:
        history = history[-20:]
    save_history(history)
