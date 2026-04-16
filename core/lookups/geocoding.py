from collections import OrderedDict

import phonenumbers
from phonenumbers import geocoder

from core.lookups.base import BaseLookup


class GeocodingLookup(BaseLookup):

    @property
    def name(self):
        return "Geolocation Lookup"

    @property
    def description(self):
        return "Get lat/lng coordinates for phone number location (no API key needed)"

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

        location = geocoder.description_for_number(parsed, "en")
        country = geocoder.country_name_for_number(parsed, "en")
        region_code = phonenumbers.region_code_for_number(parsed)
        formatted = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

        if not location and not country:
            data = OrderedDict([
                ("Phone Number", formatted),
                ("Location", "N/A"),
                ("Note", "No location data available for this number"),
            ])
            return {"success": True, "data": data, "error": None}

        # Build geocoding query
        query = f"{location}, {country}" if location and country else (location or country)

        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": query, "format": "json", "limit": "1"}
        headers = {"User-Agent": "NumDB-Lookup/2.0"}

        result = self._make_request(url, params=params, headers=headers)
        if not result["success"]:
            # Fallback: return location text without coordinates
            data = OrderedDict([
                ("Phone Number", formatted),
                ("Location", location if location else "N/A"),
                ("Country", country if country else "N/A"),
                ("Region Code", region_code if region_code else "N/A"),
                ("Latitude", "N/A (geocoding failed)"),
                ("Longitude", "N/A (geocoding failed)"),
            ])
            return {"success": True, "data": data, "error": None}

        raw = result["data"]
        if isinstance(raw, list) and len(raw) > 0:
            geo = raw[0]
            lat = geo.get("lat", "N/A")
            lon = geo.get("lon", "N/A")
            display_name = geo.get("display_name", "N/A")
            bbox = geo.get("boundingbox", [])
            bbox_str = ", ".join(bbox) if bbox else "N/A"
        else:
            lat = "N/A"
            lon = "N/A"
            display_name = "N/A"
            bbox_str = "N/A"

        data = OrderedDict([
            ("Phone Number", formatted),
            ("Location", location if location else "N/A"),
            ("Country", country if country else "N/A"),
            ("Region Code", region_code if region_code else "N/A"),
            ("Latitude", str(lat)),
            ("Longitude", str(lon)),
            ("Full Address", display_name),
            ("Bounding Box", bbox_str),
        ])

        return {"success": True, "data": data, "error": None}
