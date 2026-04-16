from .constants import GREEN, CYAN, YELLOW, RESET

def print_help():
    """Prints the help menu with available commands."""
    print(f"\n{GREEN}Termai - A CLI AI Assistant{RESET}")
    print(f"A lightweight CLI tool for AI integration in your terminal.\n")
    
    print(f"{YELLOW}Usage:{RESET}")
    print(f"  ai [OPTIONS] \"YOUR QUERY\"")
    print(f"  cat file.txt | ai [OPTIONS] \"OPTIONAL PROMPT\"")
    
    print(f"\n{YELLOW}Options:{RESET}")
    print(f"  {CYAN}--config{RESET}        Open configuration file")
    print(f"  {CYAN}--debug{RESET}         Enable debug mode")
    print(f"  {CYAN}--debug-config{RESET}  Print the loaded configuration (redacts keys)")
    print(f"  {CYAN}--help, -h{RESET}      Show this help message")
    print(f"  {CYAN}--reinstall{RESET}    Re-run the first-time setup")
    
    print(f"\n{YELLOW}Examples:{RESET}")
    print(f"  ai \"How do I unzip a tar file?\"")
    print(f"  ai --config")
    print(f"  cat error.log | ai \"Explain this error briefly\"")
    return 0 # Return 0 for success
