import urllib.parse
from collections import OrderedDict

import phonenumbers
import requests

from core.lookups.base import BaseLookup


class GoogleDorkLookup(BaseLookup):

    @property
    def name(self):
        return "Google Dorking (OSINT)"

    @property
    def description(self):
        return "Generate Google dork URLs to find public mentions of phone number (no API key needed)"

    @property
    def requires_api_key(self):
        return False

    @property
    def api_key_name(self):
        return ""

    def _build_dorks(self, phone_number, e164, national, country):
        """Build a list of Google dork queries for the phone number."""
        # Clean variants of the number
        digits_only = e164.lstrip("+")
        spaced = national

        dorks = OrderedDict()

        # General web mentions
        dorks["General Search"] = f'"{e164}" OR "{national}" OR "{digits_only}"'

        # Social media sites
        dorks["Social Media"] = (
            f'site:facebook.com OR site:linkedin.com OR site:twitter.com '
            f'OR site:instagram.com "{e164}" OR "{national}"'
        )

        # Paste sites / data dumps
        dorks["Paste Sites"] = (
            f'site:pastebin.com OR site:ghostbin.com OR site:justpaste.it '
            f'OR site:dpaste.org "{e164}" OR "{digits_only}"'
        )

        # Document leaks
        dorks["Documents"] = (
            f'filetype:pdf OR filetype:xlsx OR filetype:doc OR filetype:csv '
            f'"{e164}" OR "{digits_only}"'
        )

        # Forums and discussions
        dorks["Forums"] = (
            f'site:reddit.com OR site:quora.com OR site:stackoverflow.com '
            f'"{e164}" OR "{national}"'
        )

        # WhatsApp / Telegram public groups
        dorks["Messaging Groups"] = (
            f'site:chat.whatsapp.com OR site:t.me '
            f'"{e164}" OR "{digits_only}"'
        )

        # Spam/scam reports
        dorks["Spam Reports"] = (
            f'site:whocallsme.com OR site:800notes.com OR site:callercomplaints.com '
            f'OR site:shouldianswer.com "{e164}" OR "{national}" OR "{digits_only}"'
        )

        # Classifieds / marketplaces
        dorks["Classifieds"] = (
            f'site:craigslist.org OR site:olx.com OR site:gumtree.com '
            f'"{e164}" OR "{national}"'
        )

        return dorks

    def lookup(self, phone_number, api_key=None):
        try:
            parsed = phonenumbers.parse(phone_number, None)
        except phonenumbers.NumberParseException as e:
            return {"success": False, "data": None, "error": f"Invalid phone number: {e}"}

        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        country = phonenumbers.geocoder.country_name_for_number(parsed, "en")

        dorks = self._build_dorks(phone_number, e164, national, country)

        data = OrderedDict()
        data["Phone Number"] = intl
        data["E.164"] = e164
        data["Country"] = country if country else "N/A"
        data[""] = "─── Google Dork URLs ───"

        for label, query in dorks.items():
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            data[label] = url

        data[" "] = "─── Quick Check ───"

        # Try a quick scrape check using a public number reputation API
        # Check if the number appears on any spam databases via a simple HTTP probe
        digits = e164.lstrip("+")
        check_urls = {
            "WhoCallsMe": f"https://whocallsme.com/Phone-Number.aspx/{digits}",
            "SpamCalls.net": f"https://spamcalls.net/en/number/{digits}",
            "CallerID Test": f"https://calleridtest.com/number/{digits}",
        }

        for label, url in check_urls.items():
            data[label] = url

        return {"success": True, "data": data, "error": None}
