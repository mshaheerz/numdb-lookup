from collections import OrderedDict

from core.lookups.base import BaseLookup


class NeutrinoLookup(BaseLookup):

    @property
    def name(self):
        return "Neutrino API"

    @property
    def description(self):
        return "Phone validation with HLR data via Neutrino (key format: userid|apikey)"

    @property
    def requires_api_key(self):
        return True

    @property
    def api_key_name(self):
        return "neutrino"

    def lookup(self, phone_number, api_key=None):
        parts = api_key.split("|", 1)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return {
                "success": False,
                "data": None,
                "error": "Neutrino API key must be in format 'userid|apikey'",
            }

        user_id, actual_key = parts

        url = "https://neutrinoapi.net/phone-validate"
        params = {"number": phone_number}
        headers = {"user-id": user_id, "api-key": actual_key}

        result = self._make_request(url, params=params, headers=headers)
        if not result["success"]:
            return result

        raw = result["data"]
        if raw.get("api-error"):
            return {
                "success": False,
                "data": None,
                "error": f"API error: {raw.get('api-error-msg', raw['api-error'])}",
            }

        data = OrderedDict([
            ("Phone Number", raw.get("international-number", phone_number)),
            ("Valid", str(raw.get("valid", "N/A"))),
            ("Intl Number", raw.get("international-number", "N/A") or "N/A"),
            ("Local Number", raw.get("local-number", "N/A") or "N/A"),
            ("Country", raw.get("country", "N/A") or "N/A"),
            ("Country Code", str(raw.get("country-code", "N/A"))),
            ("Calling Code", str(raw.get("international-calling-code", "N/A"))),
            ("Location", raw.get("location", "N/A") or "N/A"),
            ("Carrier", raw.get("carrier", "N/A") or "N/A"),
            ("Type", raw.get("type", "N/A") or "N/A"),
            ("Is Mobile", str(raw.get("is-mobile", "N/A"))),
            ("Prefix Network", raw.get("prefix-network", "N/A") or "N/A"),
            ("Currency Code", raw.get("currency-code", "N/A") or "N/A"),
            ("HLR Valid", str(raw.get("hlr-valid", "N/A"))),
            ("HLR Status", raw.get("hlr-status", "N/A") or "N/A"),
            ("Current Network", raw.get("current-network", "N/A") or "N/A"),
            ("Original Network", raw.get("original-network", "N/A") or "N/A"),
            ("Ported Network", raw.get("ported-network", "N/A") or "N/A"),
            ("Roaming Country Code", raw.get("roaming-country-code", "N/A") or "N/A"),
        ])

        return {"success": True, "data": data, "error": None}
