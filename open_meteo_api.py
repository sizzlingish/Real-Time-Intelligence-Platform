import requests


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def geocode_location(location):
    params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(
            GEOCODING_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Location search failed: {e}"
        )

    results = data.get("results", [])

    if not results:
        raise ValueError(
            f"Could not find location: {location}"
        )

    place = results[0]

    return {
        "name": place.get("name"),
        "country": place.get("country"),
        "latitude": place.get("latitude"),
        "longitude": place.get("longitude")
    }


def fetch_weather(location=None, latitude=None, longitude=None):

    if location:
        place = geocode_location(location)

        latitude = place["latitude"]
        longitude = place["longitude"]

    if latitude is None or longitude is None:
        raise ValueError(
            "Please provide a location or coordinates."
        )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "weather_code"
        )
    }

    try:
        response = requests.get(
            OPEN_METEO_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Open-Meteo API request failed: {e}"
        )

    return data
