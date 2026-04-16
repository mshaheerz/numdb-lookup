from collections import OrderedDict

from core.lookups.base import BaseLookup


class NumLookupAPILookup(BaseLookup):

    @property
    def name(self):
        return "NumLookupAPI"

    @property
    def description(self):
        return "Phone validation and caller info via NumLookupAPI (requires API key)"

    @property
    def requires_api_key(self):
        return True

    @property
    def api_key_name(self):
        return "numlookupapi"

    def lookup(self, phone_number, api_key=None):
        url = f"https://api.numlookupapi.com/v1/validate/{phone_number}"
        params = {"apikey": api_key}

        result = self._make_request(url, params=params)
        if not result["success"]:
            return result

        raw = result["data"]
        if not raw.get("valid", True) and "error" in raw:
            return {
                "success": False,
                "data": None,
                "error": raw.get("error", "Unknown API error"),
            }

        data = OrderedDict([
            ("Phone Number", raw.get("number", phone_number)),
            ("Valid", str(raw.get("valid", "N/A"))),
            ("Local Format", raw.get("local_format", "N/A") or "N/A"),
            ("Intl Format", raw.get("international_format", "N/A") or "N/A"),
            ("Country Prefix", raw.get("country_prefix", "N/A") or "N/A"),
            ("Country Code", raw.get("country_code", "N/A") or "N/A"),
            ("Country Name", raw.get("country_name", "N/A") or "N/A"),
            ("Carrier", raw.get("carrier", "N/A") or "N/A"),
            ("Line Type", raw.get("line_type", "N/A") or "N/A"),
        ])

        return {"success": True, "data": data, "error": None}
