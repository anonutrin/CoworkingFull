START = 'start'
START_BTN = 'Запустить'
FILTER_SPHERE = 'Сфера'
FILTER_PRICE = "Цена"
FILTERS = 'Фильтры'
OBJECTS_MAP = 'Поиск рабочего пространства'
RESET = 'Сбросить фильтры'
SHOW_HOTEL = 'show_hotel'
# Callback queries
__SH = '_sh'
__BACK = '_back'
__DEL = '_del'
__EDIT = '_edit'

COLORIST = 'Колорист'
HAIRDRESSER = 'Парикмахер'
VISAGISTE = 'Визажист'
MAKE_UP = 'Макияж'
MANICURE = 'Маникюр'
ALL = 'Все'

HELP = 'help'
BOT_ACTIVATIONS = 'bot_activations'
ADD_ADMIN = 'addAdmin'
ADD_HOTEL = '📥 Добавление локаций'
ARROW_LEFT = '⬅'
ARROW_RIGHT = '➡'
CANCEL = 'Отменить'
CATALOG_MANAGE = 'Управление каталогом'
CHANGE_HOTEL_DATA = 'chg-hotel'
CHANGE_LOCATION = 'Изменить местоположение'
CHOOSE_ACTION = 'choose-action'
CONFIRM = '✅ Подтвердить'
CONTACT_LINK = 'contact_link'
DESCRIPTION = 'description'
EXIT = 'Выйти'
FILTER_SPHERE_LIST = [MAKE_UP, MANICURE, COLORIST, VISAGISTE, HAIRDRESSER, ALL]
GO_BACK = 'Вернуться'

HOTELS_COUNT = 'hotels-count'
HOTELS_LIST = '🗂 Список локаций'
LATITUDE = 'latitude'
LOCATION = 'location'
LONGITUDE = 'longitude'

OPEN_MAP = 'Открыть карту'
NEXT = 'Следующий'
ONE_HOTEL = 'Одна локация'
PHOTOS = 'photos'
PRICE = 'price'
RM_ADMIN = 'rmAdmin'
SEVERAL_HOTELS = 'Несколько локаций'
SHORT_DESCRIPTION = 'short_description'

STATS = 'stats'
SUBSCRIBE = 'Подписаться'
TITLE = 'title'
TYPE_OF_ADDING_HOTEL = 'type-add-h'
WORK_SCHEDULE = 'work_schedule'

# promote location
SHOW_PROMOTED_LOCATION = 'Посмотреть локацию'
PROMOTE_LOCATION = 'promote_location'
YES = 'Да'
NO = 'Нет'


def start_bot_text_template():
    return f'Отлично! Теперь можем начать работу с сервисом по поиску помещений для специалистов бьюти сферы💇‍♀\n\n' \
           f'Чтобы начать поиск:\n\n' \
           f'  1. Выберите город в графе «Изменить местоположение»\n' \
           f'  2. Нажми в меню бота кнопку «Поиск рабочего пространства»\n' \
           f'  3. На карте будут отмечены все подходящие варианты. Нажав на подходящий вариант, ты увидишь стоимость аренды, фото помещения и предоставляемые условия.\n\n' \
           f'P.S. Мы будем благодарны тебе, если ты расскажешь о нас своим коллегам. Спасибо❤️'
