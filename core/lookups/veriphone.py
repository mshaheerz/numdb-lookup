from collections import OrderedDict

from core.lookups.base import BaseLookup


class VeriphoneLookup(BaseLookup):

    @property
    def name(self):
        return "Veriphone API"

    @property
    def description(self):
        return "Phone verification via Veriphone (requires API key)"

    @property
    def requires_api_key(self):
        return True

    @property
    def api_key_name(self):
        return "veriphone"

    def lookup(self, phone_number, api_key=None):
        url = "https://api.veriphone.io/v2/verify"
        params = {"phone": phone_number}
        headers = {"Authorization": f"Bearer {api_key}"}

        result = self._make_request(url, params=params, headers=headers)
        if not result["success"]:
            return result

        raw = result["data"]
        if raw.get("status") == "error":
            return {
                "success": False,
                "data": None,
                "error": raw.get("error_message", "Unknown API error"),
            }

        data = OrderedDict([
            ("Phone Number", raw.get("phone", "N/A")),
            ("Valid", str(raw.get("phone_valid", "N/A"))),
            ("E.164 Format", raw.get("e164", "N/A") or "N/A"),
            ("Country", f"{raw.get('country', 'N/A')} ({raw.get('country_code', 'N/A')})"),
            ("Country Prefix", raw.get("country_prefix", "N/A") or "N/A"),
            ("Phone Type", raw.get("phone_type", "N/A") or "N/A"),
            ("Carrier", raw.get("carrier", "N/A") or "N/A"),
            ("Phone Region", raw.get("phone_region", "N/A") or "N/A"),
        ])

        return {"success": True, "data": data, "error": None}
