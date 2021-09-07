from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
import os
import environ
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()
environ.Env.read_env()


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


API_KEY = get_env_variable('API_KEY')

def index (request):
  print(API_KEY)
  url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
  
  error_msg = ''
  message = ''
  message_class = ''

  if request.method == 'POST':
    form = CityForm(request.POST)

    if form.is_valid():
      new_city = form.cleaned_data['name']
      existing_city_count = City.objects.filter(name=new_city).count()
      if existing_city_count == 0:
        r = requests.get(url.format(new_city, API_KEY)).json()
        if r['cod'] == 200:
          form.save()
        else:
          error_msg = 'City does not exist in the world!'
      else:
        error_msg ='City already exists in the database!'

    if error_msg:
      message = error_msg
      message_class = 'is-danger'
    else:
      message = 'City added successfully!'
      message_class = 'is-success'

  form = CityForm()
  cities = City.objects.all()

  weather_data = []

  for city in cities:
    r = requests.get(url.format(city, API_KEY)).json()

    city_weather = {
      'city': city.name,
      'temperature': r['main']['temp'],
      'description': r['weather'][0]['description'],
      'icon': r['weather'][0]['icon'],
    }

    weather_data.append(city_weather)

  context = {
    'weather_data': weather_data,
    'form': form,
    'message': message,
    'message_class': message_class,
  }

  return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
  City.objects.get(name=city_name).delete()

  return redirect('home')
