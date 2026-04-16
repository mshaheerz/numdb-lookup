from collections import OrderedDict

import phonenumbers
import requests

from core.lookups.base import BaseLookup


class ReputationLookup(BaseLookup):

    @property
    def name(self):
        return "Spam/Reputation Check"

    @property
    def description(self):
        return "Check phone number reputation and spam reports (no API key needed)"

    @property
    def requires_api_key(self):
        return False

    @property
    def api_key_name(self):
        return ""

    def _check_spamhaus(self, digits):
        """Check via public spam report aggregation."""
        reports = []

        # Check nomorobo-style endpoint
        try:
            url = f"https://www.nomorobo.com/lookup/{digits}"
            resp = requests.get(url, timeout=8, headers={
                "User-Agent": "NumDB-Lookup/2.0",
            })
            if resp.status_code == 200:
                text = resp.text.lower()
                if "spam" in text or "robocall" in text or "telemarketer" in text:
                    reports.append("Nomorobo: Likely spam/robocall")
                elif "safe" in text:
                    reports.append("Nomorobo: Appears safe")
                else:
                    reports.append("Nomorobo: No clear classification")
            else:
                reports.append(f"Nomorobo: Could not check (HTTP {resp.status_code})")
        except requests.RequestException:
            reports.append("Nomorobo: Check failed")

        return reports

    def _check_should_i_answer(self, e164, digits):
        """Check shouldianswer.com for spam reports."""
        try:
            url = f"https://www.shouldianswer.com/phone-number/{digits}"
            resp = requests.get(url, timeout=8, headers={
                "User-Agent": "NumDB-Lookup/2.0",
            })
            if resp.status_code == 200:
                text = resp.text.lower()
                if "negative" in text or "spam" in text or "scam" in text:
                    return "Negative reports found"
                elif "positive" in text or "safe" in text:
                    return "Positive/safe reports"
                elif "neutral" in text:
                    return "Neutral - no clear reports"
                else:
                    return "Page found, no clear rating"
            return f"Could not check (HTTP {resp.status_code})"
        except requests.RequestException:
            return "Check failed"

    def _check_tellows(self, digits, country_code):
        """Check tellows.com for caller ratings."""
        try:
            cc = country_code.lower() if country_code else "us"
            url = f"https://www.tellows.com/num/+{digits}"
            resp = requests.get(url, timeout=8, headers={
                "User-Agent": "NumDB-Lookup/2.0",
            })
            if resp.status_code == 200:
                text = resp.text.lower()
                if "score" in text:
                    # Try to extract score
                    import re
                    score_match = re.search(r'score[:\s]*(\d+)', text)
                    if score_match:
                        score = int(score_match.group(1))
                        if score >= 7:
                            return f"Score {score}/10 - Likely spam/dangerous"
                        elif score >= 5:
                            return f"Score {score}/10 - Suspicious"
                        else:
                            return f"Score {score}/10 - Appears safe"
                return "Listed on tellows"
            return f"Could not check (HTTP {resp.status_code})"
        except requests.RequestException:
            return "Check failed"

    def lookup(self, phone_number, api_key=None):
        try:
            parsed = phonenumbers.parse(phone_number, None)
        except phonenumbers.NumberParseException as e:
            return {"success": False, "data": None, "error": f"Invalid phone number: {e}"}

        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        digits = e164.lstrip("+")
        region = phonenumbers.region_code_for_number(parsed)

        data = OrderedDict()
        data["Phone Number"] = intl
        data["E.164"] = e164

        # Spam database checks
        spam_reports = self._check_spamhaus(digits)
        for report in spam_reports:
            parts = report.split(": ", 1)
            if len(parts) == 2:
                data[parts[0]] = parts[1]
            else:
                data["Spam Check"] = report

        # Should I Answer
        data["ShouldIAnswer"] = self._check_should_i_answer(e164, digits)

        # Tellows
        data["Tellows"] = self._check_tellows(digits, region)

        # Lookup URLs for manual checking
        data[""] = "─── Manual Check URLs ───"
        data["WhoCalledMe"] = f"https://whocalledme.com/Phone-Number.aspx/{digits}"
        data["800Notes"] = f"https://800notes.com/Phone.aspx/{digits}"
        data["SpamCalls"] = f"https://spamcalls.net/en/number/{digits}"
        data["CallerComplaints"] = f"https://callercomplaints.com/Phone-Number/{digits}"
        data["Hiya"] = f"https://hiya.com/phone/{digits}"

        return {"success": True, "data": data, "error": None}
