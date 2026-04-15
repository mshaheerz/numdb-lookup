#!/usr/bin/env python3
import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from colorama import init
from core.config import ConfigManager
from core.menu import MenuSystem
from core.display import print_banner, print_info, clear_screen


def main():
    init(autoreset=True)
    clear_screen()
    print_banner()

    config = ConfigManager()
    if not config.config_path.exists():
        config.first_run_setup()

    menu = MenuSystem(config)
    menu.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_info("Interrupted. Goodbye!")
        print()
        sys.exit(0)
