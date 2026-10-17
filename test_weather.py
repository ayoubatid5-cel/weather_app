import requests
url = "https://api.open-meteo.com/v1/forecast"
params={
    "latitude" : 40.0209,
    "longitude" : -6.8416,
    "current": "temperature_2m,wind_speed_10m"
}
response = requests.get(url,params=params)
data = response.json()

print("Temperature:", data["current"]["temperature_2m"], "°C")
print("Wind speed:", data["current"]["wind_speed_10m"], "km/h")