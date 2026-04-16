from collections import OrderedDict

from core.lookups.base import BaseLookup


class LeakCheckLookup(BaseLookup):

    @property
    def name(self):
        return "LeakCheck (Breach Data)"

    @property
    def description(self):
        return "Check if phone number appears in data breaches (requires API key)"

    @property
    def requires_api_key(self):
        return True

    @property
    def api_key_name(self):
        return "leakcheck"

    def lookup(self, phone_number, api_key=None):
        clean_number = phone_number.lstrip("+").replace(" ", "").replace("-", "")
        url = f"https://leakcheck.io/api/v2/query/{clean_number}"
        headers = {"X-API-Key": api_key}

        result = self._make_request(url, headers=headers)
        if not result["success"]:
            return result

        raw = result["data"]

        if raw.get("error"):
            return {
                "success": False,
                "data": None,
                "error": raw.get("message", raw.get("error", "Unknown API error")),
            }

        found = raw.get("found", 0)
        results = raw.get("result", [])

        if not found and not results:
            data = OrderedDict([
                ("Phone Number", phone_number),
                ("Found In Breaches", "No"),
                ("Breach Count", "0"),
                ("Status", "No breaches found for this number"),
            ])
            return {"success": True, "data": data, "error": None}

        # Extract source names from results
        sources = []
        emails_found = []
        usernames_found = []

        for entry in results:
            src = entry.get("source", {})
            if isinstance(src, dict):
                source_name = src.get("name", "Unknown")
            else:
                source_name = str(src) if src else "Unknown"
            sources.append(source_name)

            email = entry.get("email", "")
            if email:
                emails_found.append(email)

            username = entry.get("username", "")
            if username:
                usernames_found.append(username)

        data = OrderedDict([
            ("Phone Number", phone_number),
            ("Found In Breaches", "Yes"),
            ("Breach Count", str(len(results))),
            ("Sources", ", ".join(sources[:10]) if sources else "N/A"),
        ])

        if emails_found:
            data["Associated Emails"] = ", ".join(set(emails_found[:5]))
        if usernames_found:
            data["Associated Usernames"] = ", ".join(set(usernames_found[:5]))

        return {"success": True, "data": data, "error": None}
