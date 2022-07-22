# https://openweathermap.org/current
import requests
import datetime
from pprint import pprint
import json

with open('config.json') as f:
    templates = json.load(f)
    open_weather_token = templates["open_weather_token"]

class Weather:
    def __init__(self, city, open_weather_token):
        self.city = city
        self.open_weather_token = open_weather_token

    def code_weather(self, code):
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F328",
        }
        return code_to_smile[code]

    def get_request(self, city, token):
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric"
        )
        return r.json()

    def get_weather(self):

        try:
            data = self.get_request(self.city, self.open_weather_token)
            pprint(data)

            city = data["name"]
            cur_weather = data["main"]["temp"]

            weater_description = data["weather"][0]["main"]

            code = self.code_weather(weater_description)

            if weater_description in code:
                wd = code[weater_description]
            else:
                wd = "роверь погоду за окном, не пойму что там за погода!"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.\
                fromtimestamp(data["sys"]["sunrise"])

            print(f"Время: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                  f"Погода в городе: {city}\n"
                  f"Температура: {int(cur_weather)} C° {wd}\n"
                  f"Влажность: {humidity}%\n"
                  f"Давление: {int(pressure / 1.333)} мм.рт.ст\n"
                  f"Ветер: {round(wind, 1)} м/с\n"
                  f"Восход солнца: {sunrise_timestamp}\n"
                  f"Закат солнца: {sunset_timestamp}\n"
                  f"Продолжительность дня: {length_of_the_day}\n"
                  f"Хорошего дня в любую погоду!!!"
                  )

        except Exception as ex:
            print(ex)
            print("Проверьте название города")

def main():
    city = input("Введите город: ")
    class_weather = Weather(city, open_weather_token)
    class_weather.get_weather()

if __name__ == '__main__':
    main()

