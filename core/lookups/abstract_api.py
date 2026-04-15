from collections import OrderedDict

from core.lookups.base import BaseLookup


class AbstractApiLookup(BaseLookup):

    @property
    def name(self):
        return "Abstract API"

    @property
    def description(self):
        return "Phone validation via Abstract API (requires API key)"

    @property
    def requires_api_key(self):
        return True

    @property
    def api_key_name(self):
        return "abstract_api"

    def lookup(self, phone_number, api_key=None):
        url = "https://phonevalidation.abstractapi.com/v1/"
        params = {"api_key": api_key, "phone": phone_number}

        result = self._make_request(url, params=params)
        if not result["success"]:
            return result

        raw = result["data"]
        if "error" in raw:
            return {
                "success": False,
                "data": None,
                "error": raw["error"].get("message", "Unknown API error"),
            }

        fmt = raw.get("format", {}) or {}
        country = raw.get("country", {}) or {}
        carrier_info = raw.get("carrier", {}) or {}

        data = OrderedDict([
            ("Phone Number", raw.get("phone", "N/A")),
            ("Valid", str(raw.get("valid", "N/A"))),
            ("Format - Local", fmt.get("local", "N/A") or "N/A"),
            ("Format - Intl", fmt.get("international", "N/A") or "N/A"),
            ("Country", f"{country.get('name', 'N/A')} ({country.get('code', 'N/A')})"),
            ("Location", raw.get("location", "N/A") or "N/A"),
            ("Carrier", carrier_info.get("name", "N/A") or "N/A"),
            ("Type", raw.get("type", "N/A") or "N/A"),
        ])

        return {"success": True, "data": data, "error": None}
