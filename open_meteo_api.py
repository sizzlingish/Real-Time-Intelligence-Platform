import requests


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_weather(
    latitude,
    longitude,
    current=True
):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
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
