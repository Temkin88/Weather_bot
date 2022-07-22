import requests
import datetime
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

with open('config.json') as f:
    templates = json.load(f)
    open_weather_token = templates["open_weather_token"]
    tg_bot_token = templates["tg_bot_token"]

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

class Weather:
    def __init__(self):
        pass

    @dp.message_handler(commands=["start"])
    async def start_command(message: types.Message):
        await message.reply("Привет! Напиши мне город и я пришлю сводку погоды")

    @dp.message_handler()
    async def get_weather(message: types.Message):
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F328",
        }

        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
            )
            data = r.json()

            city = data["name"]
            cur_weather = data["main"]["temp"]

            weater_description = data["weather"][0]["main"]
            if weater_description in code_to_smile:
                wd = code_to_smile[weater_description]
            else:
                wd = "роверь погоду за окном, не пойму что там за погода!"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

            await message.reply(
                  f"Время: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
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
        except:
            await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == '__main__':

    executor.start_polling(dp)
