import locale
from datetime import date, timedelta

import pytest

TRANSPORT_META = {
    'bus': {
        'label': 'Автобус',
        'web_prefix': 'https://bus.tutu.ru/',
        'deeplink_prefix': 'tututransportapp://feed/bus',
    },
    'train': {
        'label': 'Поезд',
        'web_prefix': 'https://www.tutu.ru/poezda/',
        'deeplink_prefix': 'tututransportapp://feed/train',
    },
}

TRANSPORT_CASES = [
    ('bus', 'Москва', 'Тула', 0, 1),
    ('bus', 'Москва', 'Ярославль', 1, 1),
    ('bus', 'Москва', 'Владимир', 2, 2),
    ('bus', 'Санкт-Петербург', 'Великий Новгород', 3, 1),
    ('bus', 'Москва', 'Рязань', 4, 1),
    ('train', 'Москва', 'Санкт-Петербург', 0, 1),
    ('train', 'Санкт-Петербург', 'Москва', 2, 2),
    ('train', 'Москва', 'Нижний Новгород', 3, 1),
    ('train', 'Москва', 'Казань', 5, 1),
    ('train', 'Москва', 'Екатеринбург', 7, 2),
]

MONTHS_RU = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря',
}

CITY_ID_MAP = {
    'Москва': 'moscow',
    'Тула': 'tula',
    'Ярославль': 'yaroslavl',
    'Владимир': 'vladimir',
    'Санкт-Петербург': 'spb',
    'Великий Новгород': 'novgorod',
    'Рязань': 'ryazan',
    'Нижний Новгород': 'nizhny',
    'Казань': 'kazan',
    'Екатеринбург': 'ekb',
}


def _date_str(days_offset: int) -> str:
    """Возвращает дату в формате «12 июня» для подстановки в запрос."""
    d = date.today() + timedelta(days=days_offset)
    current_locale = locale.setlocale(locale.LC_TIME)

    try:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        return d.strftime('%-d %B')
    except locale.Error:
        return f'{d.day} {MONTHS_RU[d.month]}'
    finally:
        locale.setlocale(locale.LC_TIME, current_locale)


def _make_queries():
    """Генерирует список параметризованных запросов с динамическими датами."""
    queries = []
    for transport_type, from_city, to_city, days_offset, passengers in TRANSPORT_CASES:
        transport = TRANSPORT_META[transport_type]
        passenger_label = 'пассажир' if passengers == 1 else 'пассажира'
        query = (
            f'{transport["label"]} {from_city} — {to_city} '
            f'{_date_str(days_offset)}, {passengers} {passenger_label}'
        )
        param_id = f'{transport_type}_{CITY_ID_MAP[from_city]}_{CITY_ID_MAP[to_city]}'

        queries.append(
            pytest.param(
                query,
                transport['web_prefix'],
                transport['deeplink_prefix'],
                id=param_id,
            )
        )

    return queries


TRANSPORT_QUERIES = _make_queries()
