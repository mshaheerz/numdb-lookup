import time
from collections import OrderedDict

import phonenumbers
import requests

from core.lookups.base import BaseLookup


class SocialMediaLookup(BaseLookup):

    @property
    def name(self):
        return "Social Media Check"

    @property
    def description(self):
        return "Check if phone number is linked to social media platforms (no API key needed)"

    @property
    def requires_api_key(self):
        return False

    @property
    def api_key_name(self):
        return ""

    def _check_whatsapp(self, e164_number):
        """Check WhatsApp presence via their web endpoint."""
        clean = e164_number.lstrip("+")
        try:
            # WhatsApp web link - if the number is on WhatsApp, this link works
            url = f"https://api.whatsapp.com/send?phone={clean}"
            resp = requests.head(url, timeout=8, allow_redirects=True)
            if resp.status_code == 200:
                return "Likely registered (link active)"
            elif resp.status_code == 302:
                return "Likely registered (redirect)"
            else:
                return f"Unknown (HTTP {resp.status_code})"
        except requests.RequestException:
            return "Check failed"

    def _check_telegram(self, e164_number):
        """Check Telegram via t.me link probe."""
        clean = e164_number.lstrip("+")
        try:
            url = f"https://t.me/+{clean}"
            resp = requests.get(url, timeout=8, allow_redirects=False)
            if resp.status_code == 200:
                return "Possible match found"
            elif resp.status_code in (301, 302):
                return "Redirect detected (may exist)"
            else:
                return "No direct match"
        except requests.RequestException:
            return "Check failed"

    def _check_viber(self, e164_number):
        """Check Viber presence."""
        clean = e164_number.lstrip("+")
        try:
            url = f"https://chatapi.viber.com/pa/info?uri={clean}"
            resp = requests.get(url, timeout=8)
            if resp.status_code == 200:
                return "Possible account found"
            else:
                return "No direct match"
        except requests.RequestException:
            return "Check failed"

    def _check_signal(self, e164_number):
        """Signal doesn't have a public lookup - return info."""
        return "No public API (privacy-focused)"

    def _check_skype(self, e164_number):
        """Check Skype directory."""
        clean = e164_number.lstrip("+")
        try:
            url = f"https://login.skype.com/json/validator?new_value=%2B{clean}"
            resp = requests.get(url, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "available":
                    return "Not registered"
                else:
                    return "Possibly registered"
            return "Unknown"
        except requests.RequestException:
            return "Check failed"

    def _check_truecaller_web(self, e164_number, country_code):
        """Generate Truecaller web lookup URL."""
        clean = e164_number.lstrip("+")
        return f"https://www.truecaller.com/search/{country_code}/{clean}"

    def lookup(self, phone_number, api_key=None):
        try:
            parsed = phonenumbers.parse(phone_number, None)
        except phonenumbers.NumberParseException as e:
            return {"success": False, "data": None, "error": f"Invalid phone number: {e}"}

        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        region = phonenumbers.region_code_for_number(parsed)
        clean = e164.lstrip("+")

        data = OrderedDict()
        data["Phone Number"] = intl
        data["E.164"] = e164
        data["Region"] = region if region else "N/A"

        # WhatsApp check
        data["WhatsApp"] = self._check_whatsapp(e164)
        time.sleep(0.5)

        # Telegram check
        data["Telegram"] = self._check_telegram(e164)
        time.sleep(0.5)

        # Viber check
        data["Viber"] = self._check_viber(e164)
        time.sleep(0.5)

        # Skype check
        data["Skype"] = self._check_skype(e164)

        # Signal
        data["Signal"] = self._check_signal(e164)

        # Useful lookup URLs
        data["Truecaller Web"] = self._check_truecaller_web(e164, region.lower() if region else "us")
        data["Sync.me"] = f"https://sync.me/search/?number=%2B{clean}"
        data["CallerID"] = f"https://www.showcaller.com/phone-number/+{clean}"
        data["Facebook"] = f"https://www.facebook.com/search/top/?q=%2B{clean}"

        return {"success": True, "data": data, "error": None}
