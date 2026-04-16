import json
from pathlib import Path

from core.display import print_success, print_warning, print_info


class ConfigManager:

    CONFIG_FILE = "config.json"

    def __init__(self):
        self.config_path = Path(__file__).resolve().parent.parent / self.CONFIG_FILE
        if self.config_path.exists():
            self.load()
        else:
            self.data = self._default_config()

    def _default_config(self):
        return {
            "api_keys": {
                "truecaller": "",
                "numverify": "",
                "abstract_api": "",
                "veriphone": "",
                "ipqualityscore": "",
                "numlookupapi": "",
                "telnyx": "",
                "neutrino": "",
                "leakcheck": "",
                "opencnam": "",
            }
        }

    def load(self):
        try:
            with open(self.config_path, "r") as f:
                self.data = json.load(f)
            if "api_keys" not in self.data:
                self.data["api_keys"] = self._default_config()["api_keys"]
            # Merge any new default keys into existing config
            default_keys = self._default_config()["api_keys"]
            for key in default_keys:
                self.data["api_keys"].setdefault(key, default_keys[key])
        except (json.JSONDecodeError, IOError):
            print_warning("Config file corrupted. Resetting to defaults.")
            self.data = self._default_config()
            self.save()

    def save(self):
        with open(self.config_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_api_key(self, service_name):
        key = self.data.get("api_keys", {}).get(service_name, "")
        return key if key else None

    def set_api_key(self, service_name, key):
        self.data.setdefault("api_keys", {})[service_name] = key
        self.save()

    def delete_api_key(self, service_name):
        if service_name in self.data.get("api_keys", {}):
            self.data["api_keys"][service_name] = ""
            self.save()

    def has_api_key(self, service_name):
        return bool(self.get_api_key(service_name))

    def get_all_keys_status(self):
        return {
            name: bool(value)
            for name, value in self.data.get("api_keys", {}).items()
        }

    def first_run_setup(self):
        print_info("Welcome! No configuration found. Creating default config...")
        self.data = self._default_config()
        self.save()
        print_success(f"Config file created at {self.config_path}")
        print_info("You can add API keys from the Settings menu.")
        print()
