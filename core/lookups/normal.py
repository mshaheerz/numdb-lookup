from collections import OrderedDict

import phonenumbers
from phonenumbers import (
    timezone, geocoder, carrier,
    PhoneNumberFormat, PhoneNumberType,
)

TYPE_MAP = {
    PhoneNumberType.MOBILE: "Mobile",
    PhoneNumberType.FIXED_LINE: "Fixed Line",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
    PhoneNumberType.TOLL_FREE: "Toll Free",
    PhoneNumberType.PREMIUM_RATE: "Premium Rate",
    PhoneNumberType.VOIP: "VoIP",
    PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
    PhoneNumberType.PAGER: "Pager",
    PhoneNumberType.UAN: "UAN",
    PhoneNumberType.SHARED_COST: "Shared Cost",
    PhoneNumberType.UNKNOWN: "Unknown",
}

COUNTRY_CODE_SOURCE_MAP = {
    phonenumbers.CountryCodeSource.FROM_NUMBER_WITH_PLUS_SIGN: "From Number (+)",
    phonenumbers.CountryCodeSource.FROM_NUMBER_WITH_IDD: "From Number (IDD)",
    phonenumbers.CountryCodeSource.FROM_NUMBER_WITHOUT_PLUS_SIGN: "From Number (no +)",
    phonenumbers.CountryCodeSource.FROM_DEFAULT_COUNTRY: "From Default Country",
    phonenumbers.CountryCodeSource.UNSPECIFIED: "Unspecified",
}

VALIDATION_MAP = {
    phonenumbers.ValidationResult.IS_POSSIBLE: "IS_POSSIBLE",
    phonenumbers.ValidationResult.IS_POSSIBLE_LOCAL_ONLY: "IS_POSSIBLE_LOCAL_ONLY",
    phonenumbers.ValidationResult.INVALID_COUNTRY_CODE: "INVALID_COUNTRY_CODE",
    phonenumbers.ValidationResult.TOO_SHORT: "TOO_SHORT",
    phonenumbers.ValidationResult.TOO_LONG: "TOO_LONG",
    phonenumbers.ValidationResult.INVALID_LENGTH: "INVALID_LENGTH",
}


from core.lookups.base import BaseLookup


class NormalLookup(BaseLookup):

    @property
    def name(self):
        return "Normal Lookup"

    @property
    def description(self):
        return "Comprehensive offline lookup using phonenumbers library (no API key needed)"

    @property
    def requires_api_key(self):
        return False

    @property
    def api_key_name(self):
        return ""

    def lookup(self, phone_number, api_key=None):
        try:
            parsed = phonenumbers.parse(phone_number, None, keep_raw_input=True)
        except phonenumbers.NumberParseException as e:
            return {"success": False, "data": None, "error": f"Invalid phone number: {e}"}

        is_valid = phonenumbers.is_valid_number(parsed)
        is_possible = phonenumbers.is_possible_number(parsed)
        possible_reason = phonenumbers.is_possible_number_with_reason(parsed)
        num_type = phonenumbers.number_type(parsed)

        # Formats
        fmt_intl = phonenumbers.format_number(parsed, PhoneNumberFormat.INTERNATIONAL)
        fmt_e164 = phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
        fmt_national = phonenumbers.format_number(parsed, PhoneNumberFormat.NATIONAL)
        fmt_rfc3966 = phonenumbers.format_number(parsed, PhoneNumberFormat.RFC3966)

        # Geo data
        time_zones = timezone.time_zones_for_number(parsed)
        location = geocoder.description_for_number(parsed, "en")
        country_name = geocoder.country_name_for_number(parsed, "en")
        carrier_name = carrier.name_for_number(parsed, "en")

        # Region and country details
        region_code = phonenumbers.region_code_for_number(parsed)
        country_code = parsed.country_code
        national_number = parsed.national_number

        # Number components
        length_of_ndc = phonenumbers.length_of_national_destination_code(parsed)
        national_str = str(national_number)
        if length_of_ndc > 0 and length_of_ndc < len(national_str):
            ndc = national_str[:length_of_ndc]
            subscriber = national_str[length_of_ndc:]
        else:
            ndc = "N/A"
            subscriber = national_str

        # Additional checks
        is_geographical = phonenumbers.is_number_geographical(parsed)
        leading_zeros = parsed.number_of_leading_zeros if parsed.number_of_leading_zeros else None
        extension = parsed.extension
        raw_input_val = parsed.raw_input
        cc_source = parsed.country_code_source

        data = OrderedDict([
            ("Phone Number", fmt_intl),
            ("E.164 Format", fmt_e164),
            ("National Format", fmt_national),
            ("RFC3966 Format", fmt_rfc3966),
            ("Valid", str(is_valid)),
            ("Possible", str(is_possible)),
            ("Possible Reason", VALIDATION_MAP.get(possible_reason, str(possible_reason))),
            ("Type", TYPE_MAP.get(num_type, "Unknown")),
            ("Country Code", str(country_code)),
            ("Country", country_name if country_name else "N/A"),
            ("Region Code", region_code if region_code else "N/A"),
            ("Is Geographical", str(is_geographical)),
            ("Area Code (NDC)", ndc),
            ("Subscriber Number", subscriber),
            ("National Number", str(national_number)),
            ("Timezone", ", ".join(time_zones) if time_zones else "N/A"),
            ("Location", location if location else "N/A"),
            ("Carrier", carrier_name if carrier_name else "N/A"),
            ("Leading Zeros", str(leading_zeros) if leading_zeros else "N/A"),
            ("Extension", extension if extension else "N/A"),
            ("Raw Input", raw_input_val if raw_input_val else "N/A"),
            ("Country Code Source", COUNTRY_CODE_SOURCE_MAP.get(cc_source, str(cc_source))),
        ])

        return {"success": True, "data": data, "error": None}
