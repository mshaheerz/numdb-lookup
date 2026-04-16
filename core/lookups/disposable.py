from collections import OrderedDict

import phonenumbers
from phonenumbers import carrier, PhoneNumberType

from core.lookups.base import BaseLookup


# Known virtual/disposable number providers and their identifiers
VIRTUAL_CARRIERS = {
    # US/Canada VoIP and virtual providers
    "google voice": "Google Voice (Virtual)",
    "google": "Google (Possible Google Voice)",
    "textnow": "TextNow (Virtual/Disposable)",
    "textfree": "TextFree (Virtual/Disposable)",
    "bandwidth.com": "Bandwidth.com (VoIP Infrastructure)",
    "bandwidth": "Bandwidth (VoIP Infrastructure)",
    "twilio": "Twilio (Programmable VoIP)",
    "vonage": "Vonage (VoIP)",
    "ringcentral": "RingCentral (VoIP)",
    "magicjack": "MagicJack (VoIP)",
    "skype": "Skype (VoIP)",
    "line2": "Line2 (Virtual)",
    "grasshopper": "Grasshopper (Virtual Business)",
    "openphone": "OpenPhone (Virtual Business)",
    "dialpad": "Dialpad (VoIP)",
    "8x8": "8x8 (VoIP)",
    "nextiva": "Nextiva (VoIP)",
    "ooma": "Ooma (VoIP)",
    "voip.ms": "VoIP.ms (VoIP)",
    "peerless": "Peerless Network (VoIP)",
    "level 3": "Level 3/Lumen (VoIP Infrastructure)",
    "lumen": "Lumen/Level 3 (VoIP Infrastructure)",
    "intelemedia": "Intelemedia (VoIP)",
    "telnyx": "Telnyx (VoIP)",
    "plivo": "Plivo (Programmable VoIP)",
    "sinch": "Sinch (VoIP)",
    "burner": "Burner (Disposable)",
    "hushed": "Hushed (Privacy Number)",
    "sideline": "Sideline (Second Number)",
    "talkatone": "Talkatone (Free VoIP)",
    "dingtone": "Dingtone (Free VoIP)",
    "freedompop": "FreedomPop (Free VoIP)",
    "textplus": "TextPlus (Free Messaging)",
    "pinger": "Pinger (TextFree/Virtual)",
    # International VoIP
    "ovh": "OVH (VoIP - France)",
    "freephoneline": "FreePhoneLine (VoIP - Canada)",
    "voip": "Generic VoIP Provider",
    "sip": "SIP Provider",
}

# Disposable SMS receiving services (these numbers are public)
DISPOSABLE_SERVICES = [
    "receive-sms-online",
    "receivesms",
    "sms-receive",
    "temp-number",
    "smsreceivefree",
]


class DisposableLookup(BaseLookup):

    @property
    def name(self):
        return "Disposable/Virtual Detection"

    @property
    def description(self):
        return "Detect virtual, VoIP, disposable, and burner phone numbers (no API key needed)"

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
        num_type = phonenumbers.number_type(parsed)
        carrier_name = carrier.name_for_number(parsed, "en")
        country_code = parsed.country_code
        national = str(parsed.national_number)
        region = phonenumbers.region_code_for_number(parsed)

        data = OrderedDict()
        data["Phone Number"] = intl
        data["E.164"] = e164
        data["Carrier"] = carrier_name if carrier_name else "Unknown"

        # Check 1: Is it a VoIP type?
        is_voip = num_type == PhoneNumberType.VOIP
        data["Phone Type"] = "VoIP" if is_voip else self._get_type_str(num_type)

        # Check 2: Known virtual carrier match
        virtual_match = self._check_virtual_carrier(carrier_name)
        data["Virtual Carrier"] = virtual_match if virtual_match else "Not detected"

        # Check 3: Number range analysis for VoIP
        range_result = self._check_number_ranges(country_code, national, region)
        data["Range Analysis"] = range_result

        # Check 4: Toll-free or premium check
        is_special = num_type in (
            PhoneNumberType.TOLL_FREE,
            PhoneNumberType.PREMIUM_RATE,
            PhoneNumberType.SHARED_COST,
            PhoneNumberType.UAN,
        )
        data["Special Number"] = "Yes" if is_special else "No"

        # Risk assessment
        risk_score = 0
        risk_factors = []

        if is_voip:
            risk_score += 40
            risk_factors.append("VoIP type detected")
        if virtual_match:
            risk_score += 30
            risk_factors.append(f"Virtual carrier: {virtual_match}")
        if "VoIP" in range_result or "Virtual" in range_result:
            risk_score += 20
            risk_factors.append("Number in VoIP range")
        if not carrier_name:
            risk_score += 10
            risk_factors.append("Unknown carrier")

        if risk_score >= 60:
            risk_level = "HIGH - Likely virtual/disposable"
        elif risk_score >= 30:
            risk_level = "MEDIUM - Possibly virtual"
        else:
            risk_level = "LOW - Likely real mobile/landline"

        data[""] = "─── Risk Assessment ───"
        data["Risk Score"] = f"{risk_score}/100"
        data["Risk Level"] = risk_level
        data["Risk Factors"] = "; ".join(risk_factors) if risk_factors else "None detected"

        # Check URLs
        data[" "] = "─── Verification URLs ───"
        digits = e164.lstrip("+")
        data["FreeCarrierLookup"] = f"https://freecarrierlookup.com/?phone={digits}"
        data["CarrierLookup"] = f"https://www.carrierlookup.com/?phone={digits}"

        return {"success": True, "data": data, "error": None}

    def _check_virtual_carrier(self, carrier_name):
        """Check if carrier matches known virtual providers."""
        if not carrier_name:
            return None
        carrier_lower = carrier_name.lower()
        for keyword, label in VIRTUAL_CARRIERS.items():
            if keyword in carrier_lower:
                return label
        return None

    def _check_number_ranges(self, country_code, national, region):
        """Analyze number range for VoIP indicators."""
        # US/Canada area code based detection
        if country_code == 1:
            area_code = national[:3] if len(national) >= 3 else ""
            # Known VoIP-heavy area codes
            voip_heavy = {"456", "500", "521", "522", "533", "544", "566", "577", "588"}
            if area_code in voip_heavy:
                return f"VoIP-heavy area code ({area_code})"

            # Toll-free ranges
            if area_code in {"800", "833", "844", "855", "866", "877", "888"}:
                return f"Toll-free number ({area_code})"

        # UK VoIP ranges
        elif country_code == 44:
            if national.startswith("56") or national.startswith("55"):
                return "UK VoIP range (055/056)"
            if national.startswith("70"):
                return "UK personal number range (070)"

        # France VoIP
        elif country_code == 33:
            if national.startswith("9"):
                return "France VoIP range (09)"

        # Germany VoIP
        elif country_code == 49:
            if national.startswith("32"):
                return "Germany VoIP range (032)"

        # India virtual
        elif country_code == 91:
            if national.startswith("140"):
                return "India virtual/telemarketing (140)"

        return "Standard number range"

    def _get_type_str(self, num_type):
        type_map = {
            PhoneNumberType.MOBILE: "Mobile",
            PhoneNumberType.FIXED_LINE: "Fixed Line",
            PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed/Mobile",
            PhoneNumberType.TOLL_FREE: "Toll Free",
            PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            PhoneNumberType.VOIP: "VoIP",
            PhoneNumberType.PERSONAL_NUMBER: "Personal",
            PhoneNumberType.PAGER: "Pager",
            PhoneNumberType.UAN: "UAN",
            PhoneNumberType.SHARED_COST: "Shared Cost",
        }
        return type_map.get(num_type, "Unknown")
