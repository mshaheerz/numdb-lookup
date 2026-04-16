import os

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

BANNER = f"""{CYAN}{BOLD}
  _   _                 ____  ____        _                _
 | \\ | |_   _ _ __ ___ |  _ \\| __ )      | |    ___   ___ | | ___   _ _ __
 |  \\| | | | | '_ ` _ \\| | | |  _ \\ _____| |   / _ \\ / _ \\| |/ / | | | '_ \\
 | |\\  | |_| | | | | | | |_| | |_) |_____| |__| (_) | (_) |   <| |_| | |_) |
 |_| \\_|\\__,_|_| |_| |_|____/|____/      |_____\\___/ \\___/|_|\\_\\\\__,_| .__/
                                                                       |_|
{RESET}{DIM}  Phone Number Intelligence Tool v3.0{RESET}
"""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(BANNER)
    print(f"{CYAN}{'=' * 65}{RESET}")
    print()


def print_success(message):
    print(f"  {GREEN}{BOLD}[+]{RESET} {GREEN}{message}{RESET}")


def print_error(message):
    print(f"  {RED}{BOLD}[-]{RESET} {RED}{message}{RESET}")


def print_info(message):
    print(f"  {CYAN}{BOLD}[*]{RESET} {CYAN}{message}{RESET}")


def print_warning(message):
    print(f"  {YELLOW}{BOLD}[!]{RESET} {YELLOW}{message}{RESET}")


def print_menu_header(title):
    width = 50
    padding = (width - len(title) - 2) // 2
    extra = (width - len(title) - 2) % 2
    print()
    print(f"  {MAGENTA}{BOLD}{'=' * width}{RESET}")
    print(f"  {MAGENTA}{BOLD}{'|'}{' ' * padding} {title} {' ' * (padding + extra)}{'|'}{RESET}")
    print(f"  {MAGENTA}{BOLD}{'=' * width}{RESET}")
    print()


def print_menu_option(number, text, extra_info=""):
    num_str = f"{CYAN}{BOLD}[{number}]{RESET}"
    text_str = f"{WHITE}{BOLD}{text}{RESET}"
    if extra_info:
        print(f"    {num_str} {text_str}  {DIM}{extra_info}{RESET}")
    else:
        print(f"    {num_str} {text_str}")


def print_separator():
    print(f"  {DIM}{'─' * 50}{RESET}")


def print_result_table(title, data):
    if not data:
        print_error("No data to display.")
        return

    items = list(data.items()) if isinstance(data, dict) else data
    max_key_len = max(len(k) for k, _ in items)
    box_width = max_key_len + max(len(str(v)) for _, v in items) + 7
    box_width = max(box_width, len(title) + 8)

    print()
    print(f"  {CYAN}┌─── {BOLD}{title}{RESET}{CYAN} {'─' * (box_width - len(title) - 5)}┐{RESET}")
    for key, value in items:
        key_str = f"{BOLD}{WHITE}{key}{RESET}"
        val_str = f"{WHITE}{value}{RESET}"
        padding = max_key_len - len(key)
        print(f"  {CYAN}│{RESET} {key_str}{' ' * padding} : {val_str}")
    print(f"  {CYAN}└{'─' * (box_width + 1)}┘{RESET}")
    print()


def print_summary_table(title, results):
    """Print a summary table for Run All Lookups.
    results: list of dicts with keys 'name', 'status' ('success'/'failed'/'skipped'), 'message'
    """
    if not results:
        return

    max_name = max(len(r["name"]) for r in results)
    max_msg = max(len(r.get("message", "")) for r in results)
    box_width = max(max_name + max_msg + 12, len(title) + 8)

    print()
    print(f"  {MAGENTA}┌─── {BOLD}{title}{RESET}{MAGENTA} {'─' * (box_width - len(title) - 5)}┐{RESET}")
    for r in results:
        name = r["name"]
        status = r["status"]
        msg = r.get("message", "")

        if status == "success":
            icon = f"{GREEN}✓{RESET}"
            status_text = f"{GREEN}Success{RESET}"
        elif status == "failed":
            icon = f"{RED}✗{RESET}"
            status_text = f"{RED}Failed{RESET}"
        else:
            icon = f"{YELLOW}⊘{RESET}"
            status_text = f"{YELLOW}Skipped{RESET}"

        name_padded = f"{WHITE}{BOLD}{name}{RESET}"
        padding = max_name - len(name)

        if msg:
            print(f"  {MAGENTA}│{RESET} {icon} {name_padded}{' ' * padding} : {status_text} ({DIM}{msg}{RESET})")
        else:
            print(f"  {MAGENTA}│{RESET} {icon} {name_padded}{' ' * padding} : {status_text}")
    print(f"  {MAGENTA}└{'─' * (box_width + 1)}┘{RESET}")
    print()


def print_section_divider(text):
    width = 50
    padding = (width - len(text) - 2) // 2
    extra = (width - len(text) - 2) % 2
    print(f"  {DIM}{'─' * padding} {text} {'─' * (padding + extra)}{RESET}")


def input_styled(prompt):
    return input(f"  {YELLOW}{BOLD}{prompt}{RESET}")
