from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.exc import GeocoderUnavailable
import streamlit as st

geolocator = Nominatim(
    user_agent="mapguard_ai_college_project"
)


def search_location(place_name):
    """Search OpenStreetMap for a place."""

    if not place_name or not place_name.strip():
        return {
            "success": False,
            "error": "Please enter a place name."
        }

    try:
        location = geolocator.geocode(
            place_name.strip(),
            timeout=10
        )

        if location is None:
            return {
                "success": False,
                "error": "Location not found. Try a more specific name."
            }

        return {
            "success": True,
            "name": location.address,
            "latitude": location.latitude,
            "longitude": location.longitude
        }

    except (GeocoderServiceError, GeocoderTimedOut):
        return {
            "success": False,
            "error": f"location search failed:{error}"
        }
