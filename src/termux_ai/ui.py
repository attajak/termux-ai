import sys
import time
import threading
from .constants import GREEN, CYAN, YELLOW, RESET


def print_help():
    """Prints the help menu with available commands."""
...

def show_loading():
    """Simple loading indicator."""
    def spinner():
        while getattr(threading.current_thread(), "do_run", True):
            for char in ['|', '/', '-', '\\']:
                sys.stdout.write(f'\r{CYAN}Thinking... {char}{RESET}')
                sys.stdout.flush()
                time.sleep(0.1)
    
    t = threading.Thread(target=spinner)
    t.do_run = True
    t.start()
    return t

def stop_loading(t):
    """Stops the loading indicator."""
    t.do_run = False
    t.join()
    sys.stdout.write('\r' + ' ' * 20 + '\r') # Clear line
    sys.stdout.flush()
