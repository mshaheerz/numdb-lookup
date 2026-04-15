from collections import OrderedDict

from core.lookups.base import BaseLookup


class NumverifyLookup(BaseLookup):

    @property
    def name(self):
        return "Numverify API"

    @property
    def description(self):
        return "Phone validation via Numverify (requires API key)"

    @property
    def requires_api_key(self):
        return True

    @property
    def api_key_name(self):
        return "numverify"

    def lookup(self, phone_number, api_key=None):
        url = "http://apilayer.net/api/validate"
        params = {"access_key": api_key, "number": phone_number}

        result = self._make_request(url, params=params)
        if not result["success"]:
            return result

        raw = result["data"]
        if "error" in raw:
            return {
                "success": False,
                "data": None,
                "error": raw["error"].get("info", "Unknown API error"),
            }

        data = OrderedDict([
            ("Phone Number", raw.get("number", "N/A")),
            ("Valid", str(raw.get("valid", "N/A"))),
            ("Local Format", raw.get("local_format", "N/A")),
            ("Intl Format", raw.get("international_format", "N/A")),
            ("Country", f"{raw.get('country_name', 'N/A')} ({raw.get('country_code', 'N/A')})"),
            ("Location", raw.get("location", "N/A") or "N/A"),
            ("Carrier", raw.get("carrier", "N/A") or "N/A"),
            ("Line Type", raw.get("line_type", "N/A") or "N/A"),
        ])

        return {"success": True, "data": data, "error": None}
