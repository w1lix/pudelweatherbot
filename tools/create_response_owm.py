from aiohttp import ClientSession

from config import API_KEY


# получение координат
async def get_data_first(city_name: str):
    async with ClientSession() as session:
        url = f'https://api.openweathermap.org/data/2.5/weather?&lang=ru&q={city_name}&appid={API_KEY}&units=metric'
        async with session.get(url, timeout=10) as response:
            req = await response.json()
            lat = req['coord']['lat']
            lon = req['coord']['lon']

            return [lat, lon], req


# получение json на завтрашнюю погоду
async def get_data_tomorrow(coord: list) -> dict:
    async with ClientSession() as session:
        part = 'minutely,hourly,current,alerts'
        lat, lon = coord[0], coord[1]

        url = f'https://api.openweathermap.org/data/2.5/onecall?&lang=ru&lat={lat}&lon={lon}&exclude={part}&appid={API_KEY}&units=metric'

        async with session.get(url, timeout=10) as response:
            req = await response.json()

            return req['daily'][1]


# получение json на текущую погоду
async def get_data_now(coord: list) -> dict:
    async with ClientSession() as session:
        part = 'minutely,hourly,daily,alerts'
        lat, lon = coord[0], coord[1]

        url = f'https://api.openweathermap.org/data/2.5/onecall?&lang=ru&lat={lat}&lon={lon}&exclude={part}&appid={API_KEY}&units=metric'

        async with session.get(url, timeout=10) as response:
            req = await response.json()

            return req['current']
