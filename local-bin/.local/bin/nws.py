import requests
import json
import sys
from datetime import datetime

def jprint(obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        return text
def get_box_nums(lat, long):
    response = requests.get(f"https://api.weather.gov/points/{lat},{long}")
    if(response.status_code != 200):
        print(f"Error {response.status_code}")
        return (-1, -1)
    else:
        box_x = jprint(response.json()['properties']['gridX'])
        box_y = jprint(response.json()['properties']['gridY'])
        return(box_x, box_y)
def get_city(lat, long):
    response = requests.get(f"https://api.weather.gov/points/{lat},{long}")
    if(response.status_code != 200):
        print(f"Error {response.status_code}")
        return (-1, -1)
    else:
        city = jprint(response.json()['properties']['relativeLocation']['properties']['city'])
        state = jprint(response.json()['properties']['relativeLocation']['properties']['state'])
        return (city, state)
def get_temp(box_x, box_y):
    response = requests.get(f"https://api.weather.gov/gridpoints/BOX/{box_x},{box_y}/forecast/hourly")
    if(response.status_code != 200):
        return f"Error {response.status_code}"
    else:
        return jprint(response.json()['properties']['periods'][0]['temperature'])
def get_forecast(box_x, box_y):
    response = requests.get(f"https://api.weather.gov/gridpoints/BOX/{box_x},{box_y}/forecast/hourly")
    if(response.status_code != 200):
        return f"Error {response.status_code}"
    else:
        text = jprint(response.json()['properties']['periods'][0]['shortForecast'])
        return text[1:len(text)-1]
def get_date_of_forecast(box_x, box_y, hour_offset):
    response = requests.get(f"https://api.weather.gov/gridpoints/BOX/{box_x},{box_y}/forecast/hourly")
    if(response.status_code != 200):
        return f"Error {response.status_code}"
    else:
        date = jprint(response.json()['properties']['periods'][hour_offset]['startTime'])
        date = date.split('T')[0][1:]
        return date
def emojify(forecast):
    emojis = {"Mostly Clear": "🌕", "Sunny" : "☀️", "Mostly Sunny": "☀️",
    "Partly Cloudy": "⛅", "Partly Sunny": "⛅", "Rain Showers": "🌧️", "Chance Rain Showers": "Chance 🌧️", 
    "Slight Chance Rain Showers": "Slight Chance 🌧️",
    "Showers And Thunderstorms": "⛈️", "Chance Showers And Thunderstorms": "Chance ⛈️", 
    "Patchy Fog": "🌁", "Rain Showers Likely": "🌧️ Likely", "Clear": "🌕"}
    if forecast in emojis:
        return emojis[forecast]
    else:
        return forecast
def get_hourly_forecasts(box_x, box_y):
    response = requests.get(f"https://api.weather.gov/gridpoints/BOX/{box_x},{box_y}/forecast/hourly")
    results = []
    if(response.status_code != 200):
        return [f"Error {response.status_code}"]
    else:
        for elem in response.json()['properties']['periods']:
            time = jprint(elem['startTime'].split('T')[1].split('-')[0])
            time = time[1:-1]
            results.append(f"{time} : {jprint(elem['temperature'])}°F, {emojify(jprint(elem['shortForecast'])[1:-1])}")
        return results

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print("Usage: box_x and box_y")
    else:
        city = ""
        if(len(sys.argv) > 3):
            city = city.join([(item + ' ') for item in sys.argv[3:]])
        box_x = int(sys.argv[1])
        box_y = int(sys.argv[2])
        print(f"{city}: {get_temp(int(sys.argv[1]), int(sys.argv[2]))}°F, {get_forecast(box_x, box_y)}")
