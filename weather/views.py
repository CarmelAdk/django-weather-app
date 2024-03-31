import json
from django.shortcuts import render
import requests

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from .models import City
from .forms import CityForm

def get_city_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=fr&appid=ae3be71be8d31a5c9468dad29db0653e'
    response = requests.get(url.format(city)).json()
    if response['cod'] != 200:
        return None

    city_weather = {
        'city': city,
        'temperature': response['main']['temp'],
        'description': response['weather'][0]['description'].capitalize(),
        'icon': response['weather'][0]['icon'],
    }
    return city_weather

def index(request):
    return render(request, 'weather/index.html')


def cities_list(request):
    weather_data = []
    cities = City.objects.all()

    for city in cities:
        city_weather = get_city_weather(city)
        weather_data.append(city_weather) 
    
    context = {'weather_data' : weather_data}
    return render(request, 'weather/cities_list.html', context)

def add_city(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "cityListChanged": None,
                        "showMessage": f"{city.name} added."
                    })
                })
    else:
        form = CityForm()
    return render(request, 'weather/city_form.html', {
        'form': form,
    })
