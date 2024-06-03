from dataclasses import dataclass


class BaseConstants:
    @classmethod
    def get_choices(cls):
        return [
            (getattr(cls, attr), getattr(cls, attr))
            for attr in dir(cls)
            if not callable(getattr(cls, attr)) and not attr.startswith("__")
        ]

    @classmethod
    def get_choice_max_length(cls):
        return max(max(len(str(choice[0])), len(str(choice[1]))) for choice in cls.get_choices())

    @classmethod
    def get_fields(cls, exclude=None):
        if exclude is None:
            exclude = []

        field_names = list(cls.__annotations__.keys())

        return [field for field in field_names if field not in exclude]


@dataclass
class SupportedLocationChoice(BaseConstants):
    moscow: str = 'Москва'
    saint_petersburg: str = 'Санкт-Петербург'
    novosibirsk: str = 'Новосибирск'


class SupportedCategoriesChoice(BaseConstants):
    all: str = 'Все'
    manicurist: str = 'Маникюр'
    visagiste: str = 'Визажист'
    hairdresser: str = 'Парикмахер'
    colorist: str = 'Колорист'


class ConstantsTelegramUser(BaseConstants):
    user_id: str = 'User ID'
    username: str = '@username'
    is_admin: str = 'Admin'
    chose_location: str = 'Выбрана локация'
    bot_activation_count: str = 'Кол-во активаций'
    created_at: str = 'Created at'
    updated_at: str = 'Updated at'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ConstantsLocation(BaseConstants):
    id: str = 'ID'
    title: str = 'Название'
    description: str = 'Описание'
    short_description: str = 'Краткое описание (для карты)'
    price: str = 'Цена'
    price_number: str = 'Цена (Число)'
    contact_link: str = 'Контактная ссылка'
    emodji: str = 'Emodji :)'
    work_schedule: str = 'График работы'
    latitude: str = 'Долгота'
    longitude: str = 'Широта'
    full_address: str = 'Полный адрес'
    category: str = 'Категория'
    views_count: str = 'Просмотров'

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class ConstantsAuto(BaseConstants):
    id: str = 'ID'
    brand: str = 'Марка'
    model: str = 'Модель'
    equipment: str = 'Комплектация'
    year_of_issue: str = 'Год выпуска'
    class_type: str = 'Класс'
    color: str = 'Цвет'
    body: str = 'Кузов'
    drive_unit: str = 'Привод'
    fuel_type: str = 'Тип топлива'
    transmission: str = 'Коробка передач'
    power: str = 'Мощность л.с.'
    volume_engine: str = 'Объем двигателя'
    fuel_volume: str = 'Объем топлива'
    acceleration_to100: str = 'Разгон до 100'
    seats_number: str = 'Кол-во посадочных мест'
    city: str = 'Город'
    rent_cost_per_day: str = 'Стоимость аренды 1-2 суток'
    rent_cost_per_month: str = 'Стоимость аренды 30+ дней'
    description: str = 'Описание'
    links: str = 'Ссылки на авто'

    class Meta:
        verbose_name = 'Авто'
        verbose_name_plural = 'Автомобили'


class ConstantsLocationVisitStats(BaseConstants):
    user: str = 'Пользователь'
    location: str = 'Локация'
    visit_count: str = 'Переходов'
    created_at: str = 'Создано'
    updated_at: str = 'Обновлено'

    class Meta:
        verbose_name = 'Статистика локаций'
        verbose_name_plural = 'Статистика локаций'


class ConstantsBotActivationStat(BaseConstants):
    date_activation: str = 'Дата'
    activation_count: str = 'Кол-во активаций'

    class Meta:
        verbose_name = 'Статистика активаций'
        verbose_name_plural = 'Статистика активаций'
