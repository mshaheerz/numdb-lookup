from collections import OrderedDict

import phonenumbers

from core.lookups.base import BaseLookup


class CNAMLookup(BaseLookup):

    @property
    def name(self):
        return "CNAM Lookup"

    @property
    def description(self):
        return "Caller Name (CNAM) database lookup via OpenCNAM/EveryoneAPI (requires API key)"

    @property
    def requires_api_key(self):
        return True

    @property
    def api_key_name(self):
        return "opencnam"

    def lookup(self, phone_number, api_key=None):
        try:
            parsed = phonenumbers.parse(phone_number, None)
        except phonenumbers.NumberParseException as e:
            return {"success": False, "data": None, "error": f"Invalid phone number: {e}"}

        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        # Parse compound key: account_sid|auth_token
        parts = api_key.split("|", 1)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return {
                "success": False,
                "data": None,
                "error": "OpenCNAM key must be in format 'account_sid|auth_token'",
            }

        account_sid, auth_token = parts

        # OpenCNAM API
        clean = e164.lstrip("+")
        url = f"https://api.opencnam.com/v3/phone/{clean}"
        params = {
            "account_sid": account_sid,
            "auth_token": auth_token,
            "format": "json",
        }

        result = self._make_request(url, params=params)
        if not result["success"]:
            return result

        raw = result["data"]

        if raw.get("error"):
            return {
                "success": False,
                "data": None,
                "error": raw.get("error", "Unknown CNAM error"),
            }

        data = OrderedDict([
            ("Phone Number", intl),
            ("E.164", e164),
            ("Caller Name", raw.get("name", "N/A") or "N/A"),
            ("CNAM Number", raw.get("number", "N/A") or "N/A"),
            ("Price", raw.get("price", "N/A") or "N/A"),
            ("Created", raw.get("created", "N/A") or "N/A"),
            ("Updated", raw.get("updated", "N/A") or "N/A"),
        ])

        return {"success": True, "data": data, "error": None}
