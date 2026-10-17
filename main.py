
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Weather App")


@app.get("/weather")
def get_weather(latitude: float, longitude: float):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }

    try:
        result = requests.get(url, params=params, timeout=10)
        result.raise_for_status()
        data = result.json()

        current = data["current"]

        return {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "unit": "°C"
        }

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve weather data"
        )


@app.get("/weather/city")
def get_weather_by_city(city: str):

    # 1. Recherche des coordonnées de la ville
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "fr",
        "format": "json"
    }

    try:
        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Erreur lors de la recherche de la ville"
        )

    # 2. Vérifier si la ville existe
    places = geo_data.get("results", [])

    if not places:
        raise HTTPException(
            status_code=404,
            detail="Ville introuvable"
        )

    place = places[0]
    latitude = place["latitude"]
    longitude = place["longitude"]

    # 3. Récupérer la météo
    return get_weather(latitude, longitude)
