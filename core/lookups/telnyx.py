from collections import OrderedDict

from core.lookups.base import BaseLookup


class TelnyxLookup(BaseLookup):

    @property
    def name(self):
        return "Telnyx Number Lookup"

    @property
    def description(self):
        return "HLR and carrier lookup via Telnyx (requires API key)"

    @property
    def requires_api_key(self):
        return True

    @property
    def api_key_name(self):
        return "telnyx"

    def lookup(self, phone_number, api_key=None):
        url = f"https://api.telnyx.com/v2/number_lookup/{phone_number}"
        headers = {"Authorization": f"Bearer {api_key}"}

        result = self._make_request(url, headers=headers)
        if not result["success"]:
            return result

        raw = result["data"]
        # Telnyx wraps response in "data" key
        info = raw.get("data", raw)

        carrier_info = info.get("carrier", {}) or {}
        caller_name = info.get("caller_name", {}) or {}
        portability = info.get("portability", {}) or {}

        data = OrderedDict([
            ("Phone Number", info.get("phone_number", phone_number)),
            ("National Format", info.get("national_format", "N/A") or "N/A"),
            ("Country Code", info.get("country_code", "N/A") or "N/A"),
            ("Carrier Name", carrier_info.get("name", "N/A") or "N/A"),
            ("Carrier Type", carrier_info.get("type", "N/A") or "N/A"),
            ("MCC", carrier_info.get("mobile_country_code", "N/A") or "N/A"),
            ("MNC", carrier_info.get("mobile_network_code", "N/A") or "N/A"),
            ("Caller Name", caller_name.get("caller_name", "N/A") or "N/A"),
            ("Caller Name Error", caller_name.get("error_code", "None") or "None"),
            ("Line Type", portability.get("line_type", "N/A") or "N/A"),
            ("Ported Status", portability.get("ported_status", "N/A") or "N/A"),
            ("Ported Date", portability.get("ported_date", "N/A") or "N/A"),
            ("OCN", portability.get("ocn", "N/A") or "N/A"),
            ("SPID Carrier", portability.get("spid_carrier_name", "N/A") or "N/A"),
            ("SPID Carrier Type", portability.get("spid_carrier_type", "N/A") or "N/A"),
            ("City", portability.get("city", "N/A") or "N/A"),
            ("State", portability.get("state", "N/A") or "N/A"),
        ])

        return {"success": True, "data": data, "error": None}
