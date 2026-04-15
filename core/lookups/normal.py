from collections import OrderedDict

import phonenumbers
from phonenumbers import timezone, geocoder, carrier

from core.lookups.base import BaseLookup

TYPE_MAP = {
    phonenumbers.PhoneNumberType.MOBILE: "Mobile",
    phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
    phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free",
    phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
    phonenumbers.PhoneNumberType.VOIP: "VoIP",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
    phonenumbers.PhoneNumberType.PAGER: "Pager",
    phonenumbers.PhoneNumberType.UAN: "UAN",
    phonenumbers.PhoneNumberType.UNKNOWN: "Unknown",
}


class NormalLookup(BaseLookup):

    @property
    def name(self):
        return "Normal Lookup"

    @property
    def description(self):
        return "Offline lookup using phonenumbers library (no API key needed)"

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

        is_valid = phonenumbers.is_valid_number(parsed)
        num_type = phonenumbers.number_type(parsed)
        formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        time_zones = timezone.time_zones_for_number(parsed)
        location = geocoder.description_for_number(parsed, "en")
        carrier_name = carrier.name_for_number(parsed, "en")

        data = OrderedDict([
            ("Phone Number", formatted),
            ("Valid", str(is_valid)),
            ("Type", TYPE_MAP.get(num_type, "Unknown")),
            ("Timezone", ", ".join(time_zones) if time_zones else "N/A"),
            ("Location", location if location else "N/A"),
            ("Carrier", carrier_name if carrier_name else "N/A"),
        ])

        return {"success": True, "data": data, "error": None}
