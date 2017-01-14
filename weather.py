import requests

class Weather:
    def __init__(self, city, unit):
        self.city = city 
        self.temp = 0
        self.temp_min = 0
        self.temp_max = 0
        self.description = ""
        self.unit = unit if unit else 'F'

    def get_temp(self, temp_c):
        temp_f = temp_c * 1.8 + 32
        if self.unit == 'C':
            return int(round(temp_c))
        else:
            return int(round(temp_f))

    def request_weather(self):
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+self.city+'&APPID=9f98f59468e08b1ba5471f67a49dfc00&units=metric')
        try:
            o = r.json()
        except:
            return False

        for i in o:
            if i == "main":
                self.temp = self.get_temp(o[i]['temp'])
                self.temp_min = self.get_temp(o[i]['temp_min'])
                self.temp_max = self.get_temp(o[i]['temp_max'])

            if i == "weather":
                for j in o[i]:
                    self.description = j['description']
        return True

def handle_weather(state, message_in):

    description = None
    if state is None:
        # new
        # first parse for the city
        words = message_in.split()
        city = words[-1]

        # try 3 times, if it doesn't work prompt user for city
        # question mark strip
    else:
        # expecting 1-2 words
        city = message_in

    #parse city potentially
    w = Weather(city, None)
    success = w.request_weather()

    if not success:
        message_out = "Which city again?"
        state = "weather"
    else:
        state = None
        temp = w.temp
        description = w.description
        message_out = "The temperature is {0}F, {1}.".format(temp, description)

    return (state), message_out , description
