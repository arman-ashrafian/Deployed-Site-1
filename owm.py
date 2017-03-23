# This script will be used by the server to get the weather data

import pyowm as owm

API_KEY = "065b8b40e70bde7087ff44ea0ef8d5c1"
owm = owm.OWM(API_KEY)

observation = owm.weather_at_place('San Juan Capistrano, ca, usa')
weath = observation.get_weather()

def getTemp():
    temp = weath.get_temperature('fahrenheit')['temp']
    # drop second decimal place
    temp = "{0:.1f}".format(temp)

    return float(temp)

def getTempMax():
    return weath.get_temperature('fahrenheit')['temp_max']

def getTempMin():
    return weath.get_temperature('fahrenheit')['temp_min']

def getHumidity():
    return int(weath.get_humidity())

def getStatus():
    return weath.get_detailed_status()

def getIcon():
    return weath.get_weather_icon_name()
