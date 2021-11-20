from os import stat
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.conf import settings

# Create your views here.

@api_view(['GET'])
def openApi(request, location="", lat="", lon=""):
    if request.method == "GET":
        if location != "":
            openWeather  = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={settings.APIKEY}")
        elif (lat != "") and (lon != ""):
            openWeather  = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.APIKEY}")
        else:
            return Response({"error": "Please enter a valid location details"}, status=status.HTTP_400_BAD_REQUEST)

        data = openWeather.json()

        # Returning values
        try:
            main = data["main"]
            weather = data['weather']
            cloud = data["clouds"]
            timezone = data["timezone"]
            weatherid = data["id"]
            name = data["name"]
            cod = data["cod"]
            wind = data["wind"]["speed"]
            coord = data["coord"]
            icon = f"https://openweathermap.org/img/w/{weather[0]['icon']}.png"

            image = None
            listImg = []
            if weather[0]['description']:
                descri = weather[0]['description']
                unsplash = requests.get(f'https://api.unsplash.com/search/photos?page=1&per_page=200&query={descri}&client_id={settings.CLIENT_ID}')
                unsplashImg = unsplash.json()
                unsplashImg["results"]

                for img in range(len(unsplashImg["results"])):
                    listImg.append(unsplashImg["results"][img]["urls"]["regular"])

            return Response({ 
                    "data": {
                        "name": name,
                        "id": weatherid,
                        "weather":weather,
                        "main":main,
                        "clouds": cloud,
                        "timezone": timezone,
                        "cod":cod,
                        "wind": wind,
                        "coord": coord,
                        "icon": icon,
                        "unsplash": listImg[0]
                    }
                }, 
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


        # Retrive icon from API
        