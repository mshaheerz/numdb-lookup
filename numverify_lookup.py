import requests
import argparse

def get_phone_number_details(api_key, phone_number):
    url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}"
    response = requests.get(url)
    data = response.json()
    print(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lookup phone number using Numverify API")
    parser.add_argument("--api_key", required=True, help="Numverify API key")
    args = parser.parse_args()

    phone_number = "+919746854699"  # Replace with the phone number you want to check
    get_phone_number_details(args.api_key, phone_number)