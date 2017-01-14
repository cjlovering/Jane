from pprint import pprint
import pyowm
import requests
import math

UNIT = 'F'
class weather(city):
    def __init__(city):
        self.city = city if city else "Boston,us"
        self.temp = 0
        self.temp_min = 0
        self.temp_max = 0
        self.description = ""


    def get_temp(temp_c):
        temp_f = temp_c * 1.8 + 32
        if UNIT == 'C':
            return int(round(temp_c))
        else:
            return int(round(temp_f))

    def request_weather():
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=9f98f59468e08b1ba5471f67a49dfc00&units=metric')
        o = r.json()

        for i in o:
            if i == "main":
                self.temp = get_temp(o[i]['temp'])
                self.temp_min = get_temp(o[i]['temp_min'])
                self.temp_max = get_temp(o[i]['temp_max'])

            if i == "weather":
                for j in o[i]:
                    self.description = j['description']

        return

    def request_forcast():
        r = requests.get('http://api.openweathermap.org/data/2.5/forcast?q='+city+'&APPID=9f98f59468e08b1ba5471f67a49dfc00&units=metric')
        o = r.json()

        for i in o:
            print(i)
            '''
            if i == "main":
                self.temp = get_temp(o[i]['temp'])
                self.temp_min = get_temp(o[i]['temp_min'])
                self.temp_max = get_temp(o[i]['temp_max'])

            if i == "weather":
                for j in o[i]:
                    self.description = j['description'] '''

        return
