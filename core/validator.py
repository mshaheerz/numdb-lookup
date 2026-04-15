import phonenumbers


def validate_phone_number(phone_number):
    """
    Validates and parses a phone number string.
    Returns: (is_valid, message, parsed_number_or_None)
    """
    phone_number = phone_number.strip()

    try:
        parsed = phonenumbers.parse(phone_number, None)
    except phonenumbers.NumberParseException as e:
        return False, str(e), None

    if not phonenumbers.is_valid_number(parsed):
        return False, "The phone number may not be valid", parsed

    return True, "Valid", parsed
