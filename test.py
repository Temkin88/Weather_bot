import json

# smile = "\U0001F600"
# print(smile)


with open('config.json') as f:
    templates = json.load(f)

print(templates["open_weather_token"])