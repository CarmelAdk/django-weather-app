import locale
import json
from django.shortcuts import render
import requests

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect

from .models import City
from .forms import CityForm

from . forms import CreateUserForm, LoginForm

from django.contrib.auth.decorators import login_required

# - Authentication models and functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

locale.setlocale(locale.LC_NUMERIC, 'fr_FR.utf-8') 

def get_city_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=fr&appid=ae3be71be8d31a5c9468dad29db0653e'
    response = requests.get(url.format(city)).json()
    if response['cod'] != 200:
        return None

    city_weather = {
        'city_id' : city.id,
        'city': city.name,
        'temperature': locale.format("%.2f", response['main']['temp'], grouping=True),
        'description': response['weather'][0]['description'].capitalize(),
        'icon': response['weather'][0]['icon'],
    }
    return city_weather

@login_required(login_url="login")
def index(request):
    return render(request, 'weather/index.html', context = {
        'user' : request.user
    })

@login_required(login_url="login")
def cities_list(request):
    weather_data = []
    user = request.user
    cities = user.city_set.all()

    for city in cities:
        city_weather = get_city_weather(city)
        weather_data.append(city_weather) 
    
    context = {'weather_data' : weather_data}
    return render(request, 'weather/cities_list.html', context)

@login_required(login_url="login")
def add_city(request):
    if request.method == "POST":
        form = CityForm(request.POST, user=request.user)
        if form.is_valid():
            city = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "cityListChanged": None,
                        "showMessage": f"{city.name} ajouté."
                    })
                })
    else:
        form = CityForm(user=request.user)
    return render(request, 'weather/city_form.html', {
        'form': form,
    })

@login_required(login_url="login")
def edit_city(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == "POST":
        form = CityForm(request.POST, instance=city, user=request.user)
        if form.is_valid():
            if request.user == city.user:
                city = form.save()
                return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "cityListChanged": None,
                            "showMessage": f"Mise à jour réussie."
                        })
                    })
    else:
        form = CityForm(instance=city, user=request.user)
    return render(request, 'weather/city_form.html', {
        'form': form,
        'city': city,
    })

@login_required(login_url="login")
def remove_city(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.user == city.user:
        city.delete()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "cityListChanged": None,
                    "showMessage": f"{city.name} supprimé."
                })
            })

def register(request):
    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")


    context = {'registerform':form}

    return render(request, 'weather/register.html', context=context)



def login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("index")


    context = {'loginform':form}

    return render(request, 'weather/login.html', context=context)

@login_required(login_url="login")
def logout(request):

    auth.logout(request)
    return redirect("login")







