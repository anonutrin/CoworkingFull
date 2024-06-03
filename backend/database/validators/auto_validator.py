from decimal import Decimal
from typing import Optional

from pydantic import Field, BaseModel


class AutoValidator(BaseModel):
    number: int
    brand: str = Field(max_length=256, default='', alias='Марка')
    model: str = Field(max_length=256, default='', alias='Модель')
    equipment: str = Field(default='', alias='Комплектация ')
    year_of_issue: int = Field(default='', alias='Год выпуска')
    class_type: str = Field(max_length=256, default='', alias='Класс')
    color: str = Field(max_length=256, default='', alias='Цвет')
    body: str = Field(max_length=256, default='', alias='Кузов')
    drive_unit: str = Field(max_length=256, default='', alias='Привод')
    fuel_type: str = Field(max_length=256, default='', alias='Тип топлива')
    transmission: str = Field(max_length=256, default='', alias='Коробка передач')
    power: Optional[int] = Field(default=None, alias='Мощность, л.с.')
    volume_engine: Optional[Decimal] = Field(default=None, alias='Объем двигателя, см3')
    fuel_volume: Optional[int] = Field(default=None, alias='Объем топливного бака')
    acceleration_to100: Optional[Decimal] = Field(default=None, alias='Разгон до 100 км/ч., сек')
    seats_number: Optional[int] = Field(default=None, alias='Количество посадочных мест')
    city: str = Field(max_length=256, default='', alias='Город')
    rent_cost_per_day: str = Field(max_length=256, default='', alias='Стоимость аренды 1-2 суток')
    rent_cost_per_month: str = Field(max_length=256, default='', alias='Стоимость аренды 30+ суток')
    description: str = Field(default='', alias='Описание')
    links: str = Field(default='', alias='Ссылка на авто TG')
    images_link: Optional[str] = ''
