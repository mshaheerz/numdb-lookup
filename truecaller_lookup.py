import requests
import argparse

def get_phone_number_details(api_key, phone_number):
    url = f"https://api.truecaller.com/v2/phoneInfo?phone={phone_number}&countryCode=in"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lookup phone number using Truecaller API")
    parser.add_argument("--api_key", required=True, help="Truecaller API key")
    args = parser.parse_args()

    phone_number = "+919746854699"  # Replace with the phone number you want to check
    get_phone_number_details(args.api_key, phone_number)