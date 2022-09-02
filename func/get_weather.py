import requests
from config import WEATHER_API


def get_weather(text: str) -> str:
    """ Get weather with WeatherOpenMap API"""
    location = 'Vladimir' if text in ['/weather', '⛅ Погода'] else text
    directions = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API}&units=metric&lang=ru")
    data = r.json()

    city = data['name']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    weather = data['weather'][0]['main']
    weather1 = data['weather'][0]['description']
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    pressure = data['main']['pressure']
    wind_direction = directions[data['wind']['deg'] * 8 // 360]
    
    result = (f'Погода в городе {city}:\nТемпература: {round(temp)} °C / Ощущается как _{feels_like} °C_\n'
    f'{weather} ({weather1})\n\n'
    f'_Ветер {wind} м/с, {wind_direction}\nВлажность {humidity}%\nДавление {int(pressure/1.333)} мм рт. ст._')

    return result


if __name__ == '__main__':
    print(get_weather('vladimir'))
    pass
