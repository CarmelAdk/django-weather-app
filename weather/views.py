from django.shortcuts import render
import requests

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=ae3be71be8d31a5c9468dad29db0653e'
    city = 'Los Angeles'
    response = requests.get(url.format(city)).json()
    city_weather = {
        'city': city,
        'temperature': response['main']['temp'],
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    return render(request, 'weather/index.html')
