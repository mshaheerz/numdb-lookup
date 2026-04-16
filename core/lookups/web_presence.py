import time
from collections import OrderedDict

import phonenumbers
import requests

from core.lookups.base import BaseLookup


class WebPresenceLookup(BaseLookup):

    @property
    def name(self):
        return "Web Presence Scanner"

    @property
    def description(self):
        return "Scan for phone number presence across websites and platforms (no API key needed)"

    @property
    def requires_api_key(self):
        return False

    @property
    def api_key_name(self):
        return ""

    def _probe_url(self, url, indicators=None, timeout=8):
        """Probe a URL and check for presence indicators in response."""
        try:
            resp = requests.get(url, timeout=timeout, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }, allow_redirects=True)

            if resp.status_code == 200:
                if indicators:
                    text = resp.text.lower()
                    for pos, neg in indicators:
                        if pos in text and neg not in text:
                            return "Found"
                        if neg in text:
                            return "Not found"
                return "Page accessible"
            elif resp.status_code == 404:
                return "Not found"
            elif resp.status_code == 403:
                return "Access blocked"
            elif resp.status_code == 429:
                return "Rate limited"
            else:
                return f"HTTP {resp.status_code}"
        except requests.exceptions.Timeout:
            return "Timeout"
        except requests.RequestException:
            return "Error"

    def lookup(self, phone_number, api_key=None):
        try:
            parsed = phonenumbers.parse(phone_number, None)
        except phonenumbers.NumberParseException as e:
            return {"success": False, "data": None, "error": f"Invalid phone number: {e}"}

        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        digits = e164.lstrip("+")
        national_digits = str(parsed.national_number)
        region = phonenumbers.region_code_for_number(parsed)

        data = OrderedDict()
        data["Phone Number"] = intl
        data["E.164"] = e164
        data["Digits"] = digits

        # Caller ID / People search platforms
        platforms = OrderedDict([
            ("Truecaller", f"https://www.truecaller.com/search/{(region or 'us').lower()}/{digits}"),
            ("Sync.me", f"https://sync.me/search/?number=%2B{digits}"),
            ("CallerID", f"https://www.showcaller.com/phone-number/+{digits}"),
            ("Whocalld", f"https://whocalld.com/+{digits}"),
            ("NumLookup", f"https://www.numlookup.com/phone/{e164}"),
            ("ThatsThem", f"https://thatsthem.com/phone/+{digits}"),
            ("FastPeopleSearch", f"https://www.fastpeoplesearch.com/phone/{national_digits}"),
            ("TruePeopleSearch", f"https://www.truepeoplesearch.com/resultphone?phoneno={national_digits}"),
        ])

        data[" "] = "─── People Search URLs ───"
        for name, url in platforms.items():
            data[name] = url

        # Social platforms
        data["  "] = "─── Social Platform URLs ───"
        data["Facebook Search"] = f"https://www.facebook.com/search/top/?q={digits}"
        data["Instagram"] = f"https://www.instagram.com/explore/tags/{digits}/"
        data["LinkedIn"] = f"https://www.linkedin.com/search/results/all/?keywords=%2B{digits}"
        data["Twitter/X"] = f"https://twitter.com/search?q=%22{digits}%22"

        # Business / directory lookups
        data["   "] = "─── Business Directories ───"
        data["Google Business"] = f"https://www.google.com/search?q=%22{digits}%22+site:google.com/maps"
        data["Yelp"] = f"https://www.yelp.com/search?find_desc={digits}"
        data["YellowPages"] = f"https://www.yellowpages.com/phone?phone_search_terms={national_digits}"

        # Breach / leak databases
        data["    "] = "─── Breach / Leak Check URLs ───"
        data["IntelX"] = f"https://intelx.io/?s=%2B{digits}"
        data["Dehashed"] = f"https://dehashed.com/search?query=%2B{digits}"
        data["BreachDirectory"] = f"https://breachdirectory.org/search?q=%2B{digits}"

        # Messaging apps
        data["     "] = "─── Messaging Apps ───"
        data["WhatsApp Chat"] = f"https://api.whatsapp.com/send?phone={digits}"
        data["Telegram"] = f"https://t.me/+{digits}"

        return {"success": True, "data": data, "error": None}
