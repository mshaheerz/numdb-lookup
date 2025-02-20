import phonenumbers
from phonenumbers import timezone, geocoder, carrier
import sys

def get_phone_number_details(phone_number):
    parsed_number = phonenumbers.parse(phone_number, None)
    time_zones = timezone.time_zones_for_number(parsed_number)
    geolocation = geocoder.description_for_number(parsed_number, "en")
    service_provider = carrier.name_for_number(parsed_number, "en")

    print(f"Phone Number: {phone_number}")
    print(f"Timezone: {time_zones}")
    print(f"Location: {geolocation}")
    print(f"Service Provider: {service_provider}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 normal_lookup.py <phone_number>")
        sys.exit(1)

    phone_number = sys.argv[1]
    get_phone_number_details(phone_number)