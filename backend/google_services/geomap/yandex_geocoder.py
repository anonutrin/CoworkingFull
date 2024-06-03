from typing import Optional

import aiohttp
from utils.logger import logger


class GeoLocator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None

    async def set_aiohttp_session(self):
        self.session = aiohttp.ClientSession()

    async def close_aiohttp_session(self):
        if self.session:
            await self.session.close()

    async def get_coordinates(self, address):
        url = f"https://geocode-maps.yandex.ru/1.x/?apikey={self.api_key}&geocode={address}&format=json"

        async with self.session.get(url, timeout=2) as response:
            if response.status == 200:
                data = await response.json()
                try:
                    coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
                        'pos']
                    latitude, longitude = map(float, coordinates.split())
                    logger.info(f'Успешно получено координаты по адресу: {address}: {latitude}x{longitude}')
                    return latitude, longitude
                except (KeyError, IndexError, ValueError) as e:
                    print(f"Ошибка при получении координат: {e}")
                    return None
            else:
                logger.error(f"Response status is not 200: {await response.text()}")
                return None

