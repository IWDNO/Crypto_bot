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

"""
def get_forecast(text):
    try:
        wday = {0: 'Пн', 1: 'Вт', 2: 'Ср', 3: 'Чт', 4: 'Пт', 5: 'Сб', 6: 'Вс'}
        months = {1: 'Янв', 2: 'Фев', 3: 'Мар', 4: 'Апр', 5: 'Май', 6: 'Июн', 7: 'Июл', 8: 'Авг', 9: 'Сен', 10: 'Окт', 11: 'Ноя', 12: 'Дек'}

        location = 'Vladimir' if text in ['/weather', '⛅ Погода'] else text
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"

        querystring = {"q":location,"cnt":"8","units":"metric","lang":"ru"}

        headers = {
            "X-RapidAPI-Key": "23ae694b94mshde60663923854bcp123394jsn8a655805e626",
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        data = response.json()
        city = data['city']['name']

        forecast = []
        for i in range(1, 8):
            cur = data['list'][i]
            date = datetime.fromtimestamp(cur['dt'])
            day = date.day
            month = months[date.month]
            weekday = wday[date.weekday()]
            temp_d = cur['temp']['day']
            temp_n = cur['temp']['night']
            temp_e = cur['temp']['eve']
            temp_m = cur['temp']['morn']
            pressure = int(cur['pressure'] / 1.333)
            humidity = cur['humidity']
            weather = cur['weather'][0]['description'].capitalize()
            forecast.append(
                f'{weekday}, {day} {month}:\nДенём: {temp_d} °C, Ночью: {temp_n} °C\n{weather}')
        result = '\n\n'.join(forecast)
        return f'Погода в городе {city}:\n\n{result}'
    except Exception:
        return 'Неполадки...'
"""

if __name__ == '__main__':
    print(get_weather('vladimir'))
    pass
