from django.shortcuts import render
import json
import requests
from weather.settings import API_KEY
from django.contrib import messages

def get_weather(request):
    if request.method == "POST":
        city = request.POST['city']
        print(city)
        units = 'metric'
        try:
            resp = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&q={city}&units={units}").json()
            temp = int(resp['main']['temp'])
            humidity = resp['main']['humidity']
            description = resp['weather'][0]['description']
            feels_like = int(resp['main']['feels_like'])
            country = resp['sys']['country']
            place = resp['name']
            wind = (resp['wind']['speed']) * 3.6 #m/s to km/h
            visibility = (resp['visibility']) / 1000 #m to km
            context = {
                'flag': 'true',
                'country':country,
                'place':place,
                'temp':temp,
                'humidity':humidity,
                'description':description,
                'feels_like':feels_like,
                'wind':wind,
                'visibility':visibility
                }
            return render(request,'weather/index.html',context)
        except:
            if city:
                messages.warning(request,f'{city} not found')
            else:
                messages.warning(request,f'Please provide a city name')
    return render(request,'weather/index.html',{'flag':None})
    