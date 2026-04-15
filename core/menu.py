from core.lookups import get_all_lookups
from core.validator import validate_phone_number
from core.display import (
    GREEN, RED, DIM, RESET, BOLD, WHITE,
    clear_screen, print_banner, print_menu_header, print_menu_option,
    print_separator, print_result_table, print_success, print_error,
    print_info, print_warning, input_styled,
)


class MenuSystem:

    def __init__(self, config):
        self.config = config
        self.lookups = get_all_lookups()

    def run(self):
        while True:
            self._show_main_menu()
            choice = input_styled("Enter your choice: ").strip()

            settings_num = str(len(self.lookups) + 1)
            exit_num = str(len(self.lookups) + 2)

            if choice == settings_num:
                self._settings_menu()
            elif choice == exit_num:
                print()
                print_info("Goodbye! Thanks for using NumDB-Lookup.")
                print()
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(self.lookups):
                self._run_lookup(self.lookups[int(choice) - 1])
            else:
                print_error("Invalid choice. Please try again.")
                input_styled("Press Enter to continue...")

    def _show_main_menu(self):
        clear_screen()
        print_banner()
        print_menu_header("MAIN MENU")

        for i, lookup in enumerate(self.lookups, 1):
            if lookup.requires_api_key:
                has_key = self.config.has_api_key(lookup.api_key_name)
                if has_key:
                    extra = f"(API key: {GREEN}configured{RESET})"
                else:
                    extra = f"(API key: {RED}missing{RESET})"
            else:
                extra = f"({GREEN}no API key needed{RESET})"
            print_menu_option(i, lookup.name, extra)

        print()
        print_separator()
        print()
        print_menu_option(len(self.lookups) + 1, "Settings", "")
        print_menu_option(len(self.lookups) + 2, "Exit", "")
        print()

    def _run_lookup(self, lookup):
        clear_screen()
        print_banner()
        print_menu_header(lookup.name)
        print_info(lookup.description)
        print()

        # Check API key
        api_key = None
        if lookup.requires_api_key:
            api_key = self.config.get_api_key(lookup.api_key_name)
            if not api_key:
                print_error(f"No API key configured for {lookup.name}.")
                print_info("Go to Settings to add your API key.")
                print()
                input_styled("Press Enter to return to menu...")
                return

        # Get phone number
        phone_number = input_styled("Enter phone number (e.g., +14155552671): ").strip()
        if not phone_number:
            print_error("Phone number cannot be empty.")
            input_styled("Press Enter to continue...")
            return

        # Validate
        is_valid, msg, _ = validate_phone_number(phone_number)
        if not is_valid:
            print_warning(f"Validation: {msg}")
            proceed = input_styled("Continue anyway? (y/n): ").strip().lower()
            if proceed != "y":
                return

        # Perform lookup
        print()
        print_info(f"Looking up {phone_number} via {lookup.name}...")

        result = lookup.lookup(phone_number, api_key=api_key)

        if result["success"]:
            print_result_table(f"{lookup.name} Result", result["data"])
        else:
            print()
            print_error(f"Lookup failed: {result['error']}")

        print()
        input_styled("Press Enter to return to menu...")

    def _settings_menu(self):
        while True:
            clear_screen()
            print_banner()
            print_menu_header("SETTINGS")

            print_menu_option(1, "View API Keys Status", "")
            print_menu_option(2, "Add / Edit API Key", "")
            print_menu_option(3, "Delete API Key", "")
            print_menu_option(4, "Back to Main Menu", "")
            print()

            choice = input_styled("Enter your choice: ").strip()

            if choice == "1":
                self._view_keys()
            elif choice == "2":
                self._edit_key()
            elif choice == "3":
                self._delete_key()
            elif choice == "4":
                break
            else:
                print_error("Invalid choice.")
                input_styled("Press Enter to continue...")

    def _view_keys(self):
        clear_screen()
        print_banner()
        print_menu_header("API KEYS STATUS")

        statuses = self.config.get_all_keys_status()
        if not statuses:
            print_info("No API keys configured yet.")
        else:
            for name, configured in statuses.items():
                display_name = name.replace("_", " ").title()
                if configured:
                    key = self.config.get_api_key(name)
                    masked = key[:4] + "*" * (len(key) - 4) if len(key) > 4 else "****"
                    status_str = f"{GREEN}{BOLD}Configured{RESET}"
                    print(f"    {WHITE}{BOLD}{display_name:22s}{RESET} : {status_str}  ({DIM}{masked}{RESET})")
                else:
                    status_str = f"{RED}Not set{RESET}"
                    print(f"    {WHITE}{BOLD}{display_name:22s}{RESET} : {status_str}")

        print()
        input_styled("Press Enter to continue...")

    def _edit_key(self):
        clear_screen()
        print_banner()
        print_menu_header("ADD / EDIT API KEY")

        services = list(self.config.data.get("api_keys", {}).keys())
        for i, svc in enumerate(services, 1):
            display_name = svc.replace("_", " ").title()
            has = self.config.has_api_key(svc)
            extra = f"({GREEN}has key{RESET})" if has else f"({DIM}empty{RESET})"
            print_menu_option(i, display_name, extra)

        print()
        choice = input_styled("Select service number: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(services):
            service = services[int(choice) - 1]
            display_name = service.replace("_", " ").title()
            print()
            new_key = input_styled(f"Enter API key for {display_name}: ").strip()
            if new_key:
                self.config.set_api_key(service, new_key)
                print()
                print_success(f"API key for {display_name} saved successfully!")
            else:
                print()
                print_warning("No key entered. Operation cancelled.")
        else:
            print_error("Invalid selection.")

        print()
        input_styled("Press Enter to continue...")

    def _delete_key(self):
        clear_screen()
        print_banner()
        print_menu_header("DELETE API KEY")

        services = list(self.config.data.get("api_keys", {}).keys())
        for i, svc in enumerate(services, 1):
            display_name = svc.replace("_", " ").title()
            has = self.config.has_api_key(svc)
            extra = f"({GREEN}has key{RESET})" if has else f"({DIM}empty{RESET})"
            print_menu_option(i, display_name, extra)

        print()
        choice = input_styled("Select service number to clear: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(services):
            service = services[int(choice) - 1]
            display_name = service.replace("_", " ").title()
            print()
            confirm = input_styled(f"Delete API key for {display_name}? (y/n): ").strip().lower()
            if confirm == "y":
                self.config.delete_api_key(service)
                print()
                print_success(f"API key for {display_name} deleted.")
            else:
                print()
                print_info("Cancelled.")
        else:
            print_error("Invalid selection.")

        print()
        input_styled("Press Enter to continue...")
