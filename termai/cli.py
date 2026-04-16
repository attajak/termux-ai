import sys
import json
import copy
from .constants import APP_NAME, CONFIG_FILE
from .config import load_config, open_editor
from .api import send_request
from .ui import print_help

def cli_entry_point():
    # Handle --reinstall flag first
    if "--reinstall" in sys.argv:
        if CONFIG_FILE.exists():
            print(f"[{APP_NAME}] Deleting existing config for reinstall...")
            CONFIG_FILE.unlink()
        else:
            print(f"[{APP_NAME}] No existing config found. Starting first-time setup...")
    
    config = load_config()
    
    if "--reinstall" in sys.argv:
        print(f"[{APP_NAME}] Reinstall complete.")
        return 0

    # Handle --debug-config flag
    if "--debug-config" in sys.argv:
        if not config:
            print("[Error] No configuration file found. Run `ai --reinstall` to create one.")
            return 1
        
        debug_config = copy.deepcopy(config)
        if "gemini_config" in debug_config and "api_key" in debug_config["gemini_config"]:
            key = debug_config["gemini_config"]["api_key"]
            debug_config["gemini_config"]["api_key"] = f"***{key[-4:]}" if key else ""
        if "openai_config" in debug_config and "api_key" in debug_config["openai_config"]:
            key = debug_config["openai_config"]["api_key"]
            debug_config["openai_config"]["api_key"] = f"***{key[-4:]}" if key else ""
            
        print(json.dumps(debug_config, indent=4))
        return 0

    if config is None and not sys.stdin.isatty():
        return 1
    
    if "--help" in sys.argv or "-h" in sys.argv:
        return print_help()

    if "--config" in sys.argv:
        return open_editor()

    debug_mode = "--debug" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ["--debug", "--config", "--help", "-h", "--reinstall", "--debug-config"]]

    user_input = ""
    if not sys.stdin.isatty():
        user_input = sys.stdin.read().strip()
        if args: user_input += "\n" + " ".join(args)
    elif args:
        user_input = " ".join(args)
    else:
        return print_help()

    return send_request(config, user_input, debug_mode)

def main():
    sys.exit(cli_entry_point())
