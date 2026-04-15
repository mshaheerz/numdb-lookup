from collections import OrderedDict

import phonenumbers

from core.lookups.base import BaseLookup


class TruecallerLookup(BaseLookup):

    @property
    def name(self):
        return "Truecaller API"

    @property
    def description(self):
        return "Caller identification via Truecaller (requires API key)"

    @property
    def requires_api_key(self):
        return True

    @property
    def api_key_name(self):
        return "truecaller"

    def _detect_country_code(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            return phonenumbers.region_code_for_number(parsed).lower()
        except Exception:
            return "us"

    def lookup(self, phone_number, api_key=None):
        country_code = self._detect_country_code(phone_number)
        url = "https://api.truecaller.com/v2/phoneInfo"
        params = {"phone": phone_number, "countryCode": country_code}
        headers = {"Authorization": f"Bearer {api_key}"}

        result = self._make_request(url, params=params, headers=headers)
        if not result["success"]:
            return result

        raw = result["data"]
        if "error" in raw:
            err = raw["error"]
            msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
            return {"success": False, "data": None, "error": f"API error: {msg}"}

        data = OrderedDict([
            ("Phone Number", phone_number),
            ("Country Code", country_code.upper()),
        ])
        for key, value in raw.items():
            if key != "error":
                data[key.replace("_", " ").title()] = str(value)

        return {"success": True, "data": data, "error": None}
