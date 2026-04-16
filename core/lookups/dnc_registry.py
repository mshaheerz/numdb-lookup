import urllib.parse
from collections import OrderedDict

import phonenumbers
from phonenumbers import geocoder

from core.lookups.base import BaseLookup


# Country-specific telecom data
COUNTRY_DATA = {
    "US": {
        "name": "United States",
        "regulator": "FCC (Federal Communications Commission)",
        "regulator_url": "https://www.fcc.gov/",
        "dnc_name": "National Do Not Call Registry",
        "dnc_url": "https://www.donotcall.gov/",
        "dnc_check": "https://www.donotcall.gov/verify.html",
        "complaint_url": "https://consumercomplaints.fcc.gov/hc/en-us",
        "number_plan": "NANP (North American Numbering Plan)",
        "emergency": "911",
        "portability": "Yes (LNP - Local Number Portability)",
        "mobile_format": "+1 (XXX) XXX-XXXX",
    },
    "GB": {
        "name": "United Kingdom",
        "regulator": "Ofcom",
        "regulator_url": "https://www.ofcom.org.uk/",
        "dnc_name": "Telephone Preference Service (TPS)",
        "dnc_url": "https://www.tpsonline.org.uk/",
        "dnc_check": "https://www.tpsonline.org.uk/consumers/check-your-registration",
        "complaint_url": "https://www.ofcom.org.uk/complaints/",
        "number_plan": "UK National Telephone Numbering Plan",
        "emergency": "999 / 112",
        "portability": "Yes",
        "mobile_format": "+44 7XXX XXXXXX",
    },
    "IN": {
        "name": "India",
        "regulator": "TRAI (Telecom Regulatory Authority of India)",
        "regulator_url": "https://www.trai.gov.in/",
        "dnc_name": "National Do Not Call Registry (NDNC)",
        "dnc_url": "https://www.nccptrai.gov.in/nccpregistry/",
        "dnc_check": "https://www.nccptrai.gov.in/nccpregistry/search.misc",
        "complaint_url": "https://www.nccptrai.gov.in/nccpregistry/complaint.misc",
        "number_plan": "National Numbering Plan (10-digit)",
        "emergency": "112",
        "portability": "Yes (MNP - Mobile Number Portability)",
        "mobile_format": "+91 XXXXX XXXXX",
    },
    "DE": {
        "name": "Germany",
        "regulator": "BNetzA (Bundesnetzagentur)",
        "regulator_url": "https://www.bundesnetzagentur.de/",
        "dnc_name": "Robinsonliste",
        "dnc_url": "https://www.robinsonliste.de/",
        "dnc_check": "https://www.robinsonliste.de/",
        "complaint_url": "https://www.bundesnetzagentur.de/DE/Vportal/AnfragenBeschwerden/",
        "number_plan": "German Numbering Plan",
        "emergency": "112",
        "portability": "Yes",
        "mobile_format": "+49 1XX XXXXXXXX",
    },
    "FR": {
        "name": "France",
        "regulator": "ARCEP",
        "regulator_url": "https://www.arcep.fr/",
        "dnc_name": "Bloctel",
        "dnc_url": "https://www.bloctel.gouv.fr/",
        "dnc_check": "https://www.bloctel.gouv.fr/",
        "complaint_url": "https://www.arcep.fr/",
        "number_plan": "French Numbering Plan (10-digit)",
        "emergency": "112 / 15 / 17 / 18",
        "portability": "Yes",
        "mobile_format": "+33 6XX XX XX XX / +33 7XX XX XX XX",
    },
    "AU": {
        "name": "Australia",
        "regulator": "ACMA (Australian Communications and Media Authority)",
        "regulator_url": "https://www.acma.gov.au/",
        "dnc_name": "Do Not Call Register",
        "dnc_url": "https://www.donotcall.gov.au/",
        "dnc_check": "https://www.donotcall.gov.au/consumers/consumer-check-registration/",
        "complaint_url": "https://www.donotcall.gov.au/consumers/lodge-a-complaint/",
        "number_plan": "Australian Numbering Plan",
        "emergency": "000 / 112",
        "portability": "Yes",
        "mobile_format": "+61 4XX XXX XXX",
    },
    "CA": {
        "name": "Canada",
        "regulator": "CRTC (Canadian Radio-television and Telecommunications Commission)",
        "regulator_url": "https://crtc.gc.ca/",
        "dnc_name": "National Do Not Call List (DNCL)",
        "dnc_url": "https://lnnte-dncl.gc.ca/",
        "dnc_check": "https://lnnte-dncl.gc.ca/en/Consumer/Check-your-registration",
        "complaint_url": "https://lnnte-dncl.gc.ca/en/Consumer/File-a-complaint",
        "number_plan": "NANP (North American Numbering Plan)",
        "emergency": "911",
        "portability": "Yes (WLNP)",
        "mobile_format": "+1 (XXX) XXX-XXXX",
    },
    "BR": {
        "name": "Brazil",
        "regulator": "ANATEL",
        "regulator_url": "https://www.gov.br/anatel/",
        "dnc_name": "Não Me Perturbe",
        "dnc_url": "https://www.naomeperturbe.com.br/",
        "dnc_check": "https://www.naomeperturbe.com.br/",
        "complaint_url": "https://www.gov.br/anatel/pt-br/consumidor",
        "number_plan": "Brazilian Numbering Plan",
        "emergency": "190 / 192 / 193",
        "portability": "Yes",
        "mobile_format": "+55 XX 9XXXX-XXXX",
    },
    "JP": {
        "name": "Japan",
        "regulator": "MIC (Ministry of Internal Affairs and Communications)",
        "regulator_url": "https://www.soumu.go.jp/",
        "dnc_name": "No centralized DNC",
        "dnc_url": "N/A",
        "dnc_check": "N/A",
        "complaint_url": "https://www.soumu.go.jp/",
        "number_plan": "Japanese Numbering Plan",
        "emergency": "110 / 119",
        "portability": "Yes (MNP since 2006)",
        "mobile_format": "+81 X0-XXXX-XXXX",
    },
    "AE": {
        "name": "United Arab Emirates",
        "regulator": "TDRA (Telecommunications and Digital Government Regulatory Authority)",
        "regulator_url": "https://tdra.gov.ae/",
        "dnc_name": "No centralized DNC",
        "dnc_url": "N/A",
        "dnc_check": "N/A",
        "complaint_url": "https://tdra.gov.ae/en/consumer-corner/complaints",
        "number_plan": "UAE Numbering Plan",
        "emergency": "999 / 998 / 997",
        "portability": "Yes (MNP since 2013)",
        "mobile_format": "+971 5X XXX XXXX",
    },
}


class DNCRegistryLookup(BaseLookup):

    @property
    def name(self):
        return "DNC & Country Registry"

    @property
    def description(self):
        return "Check Do Not Call registries and country-specific telecom info (no API key needed)"

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
        region = phonenumbers.region_code_for_number(parsed)
        country_name = geocoder.country_name_for_number(parsed, "en")

        data = OrderedDict()
        data["Phone Number"] = intl
        data["E.164"] = e164
        data["Country"] = country_name if country_name else "Unknown"
        data["Region Code"] = region if region else "Unknown"

        country_info = COUNTRY_DATA.get(region, None)

        if country_info:
            data[""] = "─── Telecom Regulator ───"
            data["Regulator"] = country_info["regulator"]
            data["Regulator URL"] = country_info["regulator_url"]
            data["Number Plan"] = country_info["number_plan"]
            data["Emergency Number"] = country_info["emergency"]
            data["Number Portability"] = country_info["portability"]
            data["Mobile Format"] = country_info["mobile_format"]

            data[" "] = "─── Do Not Call Registry ───"
            data["DNC Registry"] = country_info["dnc_name"]
            data["DNC URL"] = country_info["dnc_url"]
            data["Check Registration"] = country_info["dnc_check"]
            data["File Complaint"] = country_info["complaint_url"]
        else:
            data[""] = "─── Country Info ───"
            data["Regulator"] = "Not in database"
            data["Note"] = f"Country-specific data not available for {region}"

            # Generic international resources
            data[" "] = "─── International Resources ───"
            data["ITU"] = "https://www.itu.int/en/ITU-T/inr/Pages/default.aspx"
            data["World Numbering Plans"] = f"https://www.numberingplans.com/?page=plans&sub=phonenr&alpha_2_input={region}"

        # Caller complaint / lookup URLs
        data["  "] = "─── Complaint & Lookup ───"
        digits = e164.lstrip("+")
        data["Report Spam (Google)"] = f"https://www.google.com/search?q=%22{digits}%22+spam+scam"
        data["GSMA Device Check"] = "https://www.gsma.com/get-involved/working-groups/fraud-security-group"
        data["Number Lookup"] = f"https://www.numberingplans.com/?page=analysis&sub=phonenr&number={urllib.parse.quote(e164)}"

        return {"success": True, "data": data, "error": None}
