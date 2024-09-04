import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import random

load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    city: str
    country: str
    main: str
    description: str
    icon: str
    temperature: int

CITIES = [
    ("New York", "US"),
    ("London", "GB"),
    ("Tokyo", "JP"),
    ("Paris", "FR"),
    ("Berlin", "DE"),
    ("Sydney", "AU"),
    ("Moscow", "RU"),
    ("Toronto", "CA")
]

def get_random_city():
    return random.choice(CITIES)

def get_lat_lon(city_name, country_code, API_key):
    query = f'{city_name},{country_code}'
    response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={query}&appid={API_key}')
    data = response.json()
    
    print(f"Geocoding Response: {data}")  # Debug print
    
    if not data:
        return None, None
    
    data = data[0]
    return data.get('lat'), data.get('lon')

def get_current_weather(lat, lon, API_key):
    if lat is None or lon is None:
        return None

    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    if "weather" not in resp or "main" not in resp:
        return None

    return WeatherData(
        city='',  # Aquí no se establece el nombre de la ciudad
        country='',  # Aquí no se establece el nombre del país
        main=resp['weather'][0]['main'],
        description=resp['weather'][0]['description'],
        icon=resp['weather'][0]['icon'],
        temperature=int(resp['main']['temp'])
    )

    
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric')
    data = response.json()
    
    print(f"Weather Response: {data}")  
    
    if "weather" not in data or "main" not in data:
        return None

    weather_data = WeatherData(
        main=data['weather'][0]['main'],
        description=data['weather'][0]['description'],
        icon=data['weather'][0]['icon'],
        temperature=int(data['main']['temp'])
    )
    return weather_data

def main(city_name, country_name):
    lat, lon = get_lat_lon(city_name, country_name, api_key)
    if lat is None or lon is None:
        return None
    
    weather_data = get_current_weather(lat, lon, api_key)
    if weather_data:
        return WeatherData(
            city=city_name,
            country=country_name,
            main=weather_data.main,
            description=weather_data.description,
            icon=weather_data.icon,
            temperature=weather_data.temperature
        )
    return None



if __name__ == "__main__":
    city, country = get_random_city()
    lat, lon = get_lat_lon(city, country, api_key)
    print(f"City: {city}, Country: {country}, Lat: {lat}, Lon: {lon}")
    weather = get_current_weather(lat, lon, api_key)
    print(weather)
