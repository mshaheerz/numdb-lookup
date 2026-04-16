from collections import OrderedDict

import phonenumbers

from core.lookups.base import BaseLookup


class OVHTelecomLookup(BaseLookup):

    @property
    def name(self):
        return "OVH Telecom Scanner"

    @property
    def description(self):
        return "Check if number belongs to OVH VoIP ranges and get telecom data (no API key needed)"

    @property
    def requires_api_key(self):
        return False

    @property
    def api_key_name(self):
        return ""

    def lookup(self, phone_number, api_key=None):
        try:
            parsed = phonenumbers.parse(phone_number, None)
        except phonenumbers.NumberParseException as e:
            return {"success": False, "data": None, "error": f"Invalid phone number: {e}"}

        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        country_code = parsed.country_code
        region = phonenumbers.region_code_for_number(parsed)

        data = OrderedDict()
        data["Phone Number"] = intl
        data["E.164"] = e164

        # OVH Telecom API - check number ranges
        # OVH provides public API for their telecom services
        url = f"https://api.ovh.com/1.0/telephony/number/detailedZones"
        params = {"country": region.lower() if region else "fr"}

        result = self._make_request(url, params=params, timeout=10)

        if result["success"] and isinstance(result["data"], list):
            raw = result["data"]
            national = str(parsed.national_number)

            found_zone = None
            for zone in raw:
                zone_prefix = zone.get("number", "")
                if national.startswith(zone_prefix.replace("+", "")):
                    found_zone = zone
                    break

            if found_zone:
                data["OVH Zone Match"] = "Yes"
                data["Zone Number"] = found_zone.get("number", "N/A")
                data["Zone Country"] = found_zone.get("country", "N/A")
                data["Zone City"] = found_zone.get("city", "N/A")
                data["Zone Type"] = found_zone.get("type", "N/A")
                data["Zone Prefix"] = found_zone.get("prefix", "N/A")
                data["Is VoIP Range"] = "Likely (OVH zone)" if found_zone.get("type") == "voip" else "Unknown"
            else:
                data["OVH Zone Match"] = "No match in OVH ranges"
        else:
            data["OVH Zone Check"] = "Could not query OVH API"

        # Additional VoIP provider detection via number range analysis
        data[""] = "─── VoIP Range Analysis ───"

        # Check against known VoIP provider number ranges
        voip_indicators = self._check_voip_ranges(country_code, str(parsed.national_number), region)
        for key, value in voip_indicators.items():
            data[key] = value

        # OVH public number search
        data[" "] = "─── OVH Lookup URLs ───"
        clean = e164.lstrip("+")
        data["OVH Number Check"] = f"https://api.ovh.com/1.0/telephony/number/ranges?country={(region or 'fr').lower()}"
        data["Telecom Regulator"] = self._get_regulator_url(region)

        return {"success": True, "data": data, "error": None}

    def _check_voip_ranges(self, country_code, national_number, region):
        """Check if number falls in known VoIP provider ranges."""
        results = OrderedDict()

        # Common VoIP indicators by country
        voip_prefixes = {
            1: {  # US/Canada
                "Google Voice": ["205", "209", "213", "253", "310", "312", "313", "314", "347",
                                 "404", "415", "424", "470", "501", "503", "504", "505", "507",
                                 "509", "512", "513", "515", "559", "562", "570", "571", "573",
                                 "574", "575", "585", "586"],
                "TextNow": ["226", "249", "289", "365", "437", "548", "579", "581", "587",
                            "613", "639", "647", "672", "705", "709", "778", "780", "782"],
                "Bandwidth.com (VoIP)": ["833", "844", "855", "866", "877", "888"],
            },
            44: {  # UK
                "VoIP Range (056)": ["56"],
                "VoIP Range (055)": ["55"],
            },
            33: {  # France
                "OVH/VoIP (09)": ["9"],
            },
            91: {  # India
                "Virtual (140)": ["140"],
            },
        }

        country_ranges = voip_prefixes.get(country_code, {})
        matched_provider = None

        for provider, prefixes in country_ranges.items():
            for prefix in prefixes:
                if national_number.startswith(prefix):
                    matched_provider = provider
                    break
            if matched_provider:
                break

        if matched_provider:
            results["VoIP Provider Match"] = matched_provider
            results["Likely Virtual"] = "Yes"
        else:
            results["VoIP Provider Match"] = "No known VoIP range match"
            results["Likely Virtual"] = "Unknown"

        return results

    def _get_regulator_url(self, region):
        """Return the telecom regulator URL for the country."""
        regulators = {
            "US": "https://www.fcc.gov/consumers/guides/wireless-phone-number-portability",
            "GB": "https://www.ofcom.org.uk/phones-telecoms-and-internet/",
            "FR": "https://www.arcep.fr/",
            "DE": "https://www.bundesnetzagentur.de/",
            "IN": "https://www.trai.gov.in/",
            "AU": "https://www.acma.gov.au/",
            "CA": "https://crtc.gc.ca/",
            "BR": "https://www.gov.br/anatel/",
        }
        return regulators.get(region, "N/A")
