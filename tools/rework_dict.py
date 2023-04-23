from datetime import datetime

from tools.degrees_to_direction import degrees_to_direction


# переделывание словаря завтрашнего прогноза
def rework_forecast(data: dict) -> dict:
    # основные данные с температурами
    eve = round(data['temp']['eve'])
    morn = round(data['temp']['morn'])
    day = round(data['temp']['day'])
    night = round(data['temp']['night'])

    fleve = round(data['feels_like']['eve'])
    flmorn = round(data['feels_like']['morn'])
    flday = round(data['feels_like']['day'])
    flnight = round(data['feels_like']['night'])

    temp_min = round(data['temp']['min'])
    temp_max = round(data['temp']['max'])

    # восход, рассвет, световой день
    sunrise = datetime.fromtimestamp(data['sunrise'])
    sunset = datetime.fromtimestamp(data['sunset'])
    ldr = str(sunset - sunrise)[:-3].split(":")  # [:-3] - обрезает H:M:S до H:M

    # описание
    descr = data['weather'][0]['description']

    # оставшиеся данные
    clouds = data['clouds']
    humidity = data['humidity']
    pressure = data['pressure']
    dew_point = round(data['dew_point'])
    pop = round(data['pop'])

    uvi = round(data['uvi'])
    uvt = uvi_check(uvi)

    wind_speed = round(data['wind_speed'])
    wind_direction = degrees_to_direction(round(data['wind_deg']))

    res = {'eve': eve, 'morn': morn, 'day': day, 'night': night,
           'fleve': fleve, 'flmorn': flmorn, 'flday': flday, 'flnight': flnight,
           'temp_min': temp_min, 'temp_max': temp_max,

           'sunrise': sunrise, 'sunset': sunset, 'ldr': ldr,
           'descr': descr,

           'clouds': clouds, 'humidity': humidity,
           'pressure': pressure, 'dew_point': dew_point, 'pop': pop,
           'uvi': uvi, 'uvt': uvt,
           'wind_speed': wind_speed, 'wind_direction': wind_direction}

    return res


# переделывание словаря текущей погоды
def rework_now(data: dict) -> dict:
    # основные данные с температурами
    temp = round(data['temp'])
    feels_like = round(data['feels_like'])

    # описание
    descr = data['weather'][0]['description']

    # восход, рассвет, световой день
    sunrise = datetime.fromtimestamp(data['sunrise'])
    sunset = datetime.fromtimestamp(data['sunset'])
    ldr = str(sunset - sunrise)[:-3].split(":")  # [:-3] - обрезает H:M:S до H:M

    # оставшиеся данные
    clouds = round(data['clouds'])
    humidity = round(data['humidity'])
    pressure = round(data['pressure'])
    dew_point = round(data['dew_point'])
    uvi = round(data['uvi'])
    uvt = uvi_check(uvi)
    visibility = check_visibility(data['visibility'])

    wind_speed = round(data['wind_speed'])
    wind_direction = degrees_to_direction(round(data['wind_deg']))

    res = {'temp': temp, 'feels_like': feels_like,

           'sunrise': sunrise, 'sunset': sunset, 'ldr': ldr,
           'descr': descr,

           'clouds': clouds, 'humidity': humidity,
           'pressure': pressure, 'dew_point': dew_point,
           'uvi': uvi, 'uvt': uvt, 'visibility': visibility,
           'wind_speed': wind_speed, 'wind_direction': wind_direction}

    return res


# текстовое значение uvi
def uvi_check(index: int) -> str:
    if 0 <= index <= 2:
        uvt = "низкий"
    elif 3 <= index <= 5:
        uvt = 'умеренный'
    elif 6 <= index <= 7:
        uvt = 'высокий'
    elif 8 <= index <= 10:
        uvt = "оч. высокий"
    else:
        uvt = 'экстремальный'

    return uvt


# текстовое значение visibility
def check_visibility(visibility: int) -> str:
    visibility_text = "n/a"
    if visibility >= 20000:
        visibility_text = f"Видимость: Отличная"
    elif 10000 <= visibility <= 20000:
        visibility_text = f"Видимость: Хорошая"
    elif 4000 <= visibility <= 10000:
        visibility_text = f"Видимость: Средняя"
    elif 2000 <= visibility <= 4000:
        visibility_text = f"Видимость: Плохая"
    elif 0 <= visibility <= 2000:
        visibility_text = f"Видимость: Очень плохая"

    return visibility_text
