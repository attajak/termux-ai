import sys
import json
import copy
import argparse
from .constants import APP_NAME, CONFIG_FILE
from .config import load_config, open_editor
from .api import send_request
from .ui import print_help


def cli_entry_point():
    parser = argparse.ArgumentParser(
        description="Termux-AI: A lightweight CLI wrapper for Gemini and OpenAI.",
        add_help=False,  # We handle --help manually to keep UI consistent or use custom help
    )

    # Define arguments
    parser.add_argument("prompt", nargs="*", help="The prompt to send to the AI.")
    parser.add_argument(
        "--config",
        "-c",
        action="store_true",
        help="Open the configuration file in your editor.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode to see raw API responses.",
    )
    parser.add_argument(
        "--debug-config",
        action="store_true",
        help="Print the loaded configuration (keys redacted).",
    )
    parser.add_argument(
        "--reinstall",
        action="store_true",
        help="Reset configuration and re-run first-time setup.",
    )
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Enable chat mode (uses conversation history).",
    )
    # help and -h are already added correctly by the parser (standard behavior),
    # but the explicit addition here handles the custom help menu.
    parser.add_argument(
        "--help", "-h", action="store_true", help="Show this help message and exit."
    )

    # Parse arguments
    # Note: parse_known_args can be used if we want to allow unknown flags to be part of the prompt,
    # but here we'll stick to parse_args for strictness or handle prompt manually.
    args = parser.parse_args()

    # 1. Handle Help
    if args.help:
        return print_help()

    # 2. Handle Reinstall
    if args.reinstall:
        if CONFIG_FILE.exists():
            print(f"[{APP_NAME}] Deleting existing config for reinstall...")
            CONFIG_FILE.unlink()
        else:
            print(
                f"[{APP_NAME}] No existing config found. Starting first-time setup..."
            )
        # load_config() will trigger setup if file is missing
        load_config()
        print(f"[{APP_NAME}] Reinstall complete.")
        return 0

    # Load config for remaining commands
    config = load_config()

    # 3. Handle Debug Config
    if args.debug_config:
        if not config:
            print(
                "[Error] No configuration file found. Run `ai --reinstall` to create one."
            )
            return 1

        debug_config = copy.deepcopy(config)
        # Redact keys
        for provider in ["gemini_config", "openai_config"]:
            if provider in debug_config and "api_key" in debug_config[provider]:
                key = debug_config[provider]["api_key"]
                debug_config[provider]["api_key"] = f"***{key[-4:]}" if key else ""

        print(json.dumps(debug_config, indent=4))
        return 0

    # 4. Handle Config Edit
    if args.config:
        return open_editor()

    # 5. Handle Request
    from .chat import load_history, add_to_history
    
    user_input = ""
    # Check for stdin first (piping)
    if not sys.stdin.isatty():
        user_input = sys.stdin.read().strip()
        if args.prompt:
            user_input += "\n" + " ".join(args.prompt)
    elif args.prompt:
        user_input = " ".join(args.prompt)
    else:
        # No stdin and no prompt, show help
        return print_help()

    if not config and not sys.stdin.isatty():
        return 1

    history = []
    if args.chat:
        history = load_history()
        add_to_history("user", user_input)

    # Need to update send_request to accept history
    # For now, just call it. We need to update API to pass history.
    # Actually, the providers need to know how to handle history.
    
    # Simple fix: update send_request signature is better
    return send_request(config, user_input, args.debug, history=history)


def main():
    sys.exit(cli_entry_point())
