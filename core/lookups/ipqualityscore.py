from collections import OrderedDict

from core.lookups.base import BaseLookup


class IPQualityScoreLookup(BaseLookup):

    @property
    def name(self):
        return "IPQualityScore API"

    @property
    def description(self):
        return "Phone fraud scoring via IPQualityScore (requires API key)"

    @property
    def requires_api_key(self):
        return True

    @property
    def api_key_name(self):
        return "ipqualityscore"

    def lookup(self, phone_number, api_key=None):
        url = f"https://www.ipqualityscore.com/api/json/phone/{api_key}/{phone_number}"

        result = self._make_request(url)
        if not result["success"]:
            return result

        raw = result["data"]
        if not raw.get("success", True):
            return {
                "success": False,
                "data": None,
                "error": raw.get("message", "Unknown API error"),
            }

        data = OrderedDict([
            ("Phone Number", raw.get("formatted", phone_number)),
            ("Valid", str(raw.get("valid", "N/A"))),
            ("Fraud Score", str(raw.get("fraud_score", "N/A"))),
            ("Country", raw.get("country", "N/A") or "N/A"),
            ("Region", raw.get("region", "N/A") or "N/A"),
            ("City", raw.get("city", "N/A") or "N/A"),
            ("Carrier", raw.get("carrier", "N/A") or "N/A"),
            ("Line Type", raw.get("line_type", "N/A") or "N/A"),
            ("Active", str(raw.get("active", "N/A"))),
            ("VOIP", str(raw.get("VOIP", "N/A"))),
            ("Prepaid", str(raw.get("prepaid", "N/A"))),
            ("Risky", str(raw.get("risky", "N/A"))),
            ("Recent Abuse", str(raw.get("recent_abuse", "N/A"))),
            ("Spammer", str(raw.get("spammer", "N/A"))),
        ])

        return {"success": True, "data": data, "error": None}
