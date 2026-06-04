"""Тесты проверки наличия кнопки-ссылки на поиск билетов в ответе ассистента.

При запросе билетов на автобус или поезд с указанием маршрута, даты и числа пассажиров
ассистент должен вернуть ссылку в поле textMetaInfo финального сообщения.

Используются популярные маршруты с высокой вероятностью наличия рейсов.
Если ссылка не пришла — это баг.
"""

from datetime import date, timedelta
from uuid import uuid4

import pytest
import requests

from utils.attach import add_api_request, add_api_response

MOCK_MESSAGES_ENDPOINT = '/sync/messages'
SYNC_REQUEST_TIMEOUT = 120

BUS_URL_PREFIX = 'https://bus.tutu.ru/'
BUS_DEEPLINK_PREFIX = 'tututransportapp://feed/bus'
TRAIN_URL_PREFIX = 'https://www.tutu.ru/poezda/'
TRAIN_DEEPLINK_PREFIX = 'tututransportapp://feed/train'


def _date_str(days_offset: int) -> str:
    """Возвращает дату в формате «12 июня» для подстановки в запрос."""
    MONTHS = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря',
    }
    d = date.today() + timedelta(days=days_offset)
    return f'{d.day} {MONTHS[d.month]}'


def _make_queries():
    """Генерирует список параметризованных запросов с динамическими датами."""
    return [
        pytest.param(
            f'Автобус Москва — Тула {_date_str(0)}, 1 пассажир',
            BUS_URL_PREFIX,
            BUS_DEEPLINK_PREFIX,
            id='bus_moscow_tula',
        ),
        pytest.param(
            f'Автобус Москва — Ярославль {_date_str(1)}, 1 пассажир',
            BUS_URL_PREFIX,
            BUS_DEEPLINK_PREFIX,
            id='bus_moscow_yaroslavl',
        ),
        pytest.param(
            f'Автобус Москва — Владимир {_date_str(2)}, 2 пассажира',
            BUS_URL_PREFIX,
            BUS_DEEPLINK_PREFIX,
            id='bus_moscow_vladimir',
        ),
        pytest.param(
            f'Автобус Санкт-Петербург — Великий Новгород {_date_str(3)}, 1 пассажир',
            BUS_URL_PREFIX,
            BUS_DEEPLINK_PREFIX,
            id='bus_spb_novgorod',
        ),
        pytest.param(
            f'Автобус Москва — Рязань {_date_str(4)}, 1 пассажир',
            BUS_URL_PREFIX,
            BUS_DEEPLINK_PREFIX,
            id='bus_moscow_ryazan',
        ),
        pytest.param(
            f'Поезд Москва — Санкт-Петербург {_date_str(0)}, 1 пассажир',
            TRAIN_URL_PREFIX,
            TRAIN_DEEPLINK_PREFIX,
            id='train_moscow_spb',
        ),
        pytest.param(
            f'Поезд Санкт-Петербург — Москва {_date_str(2)}, 2 пассажира',
            TRAIN_URL_PREFIX,
            TRAIN_DEEPLINK_PREFIX,
            id='train_spb_moscow',
        ),
        pytest.param(
            f'Поезд Москва — Нижний Новгород {_date_str(3)}, 1 пассажир',
            TRAIN_URL_PREFIX,
            TRAIN_DEEPLINK_PREFIX,
            id='train_moscow_nizhny',
        ),
        pytest.param(
            f'Поезд Москва — Казань {_date_str(5)}, 1 пассажир',
            TRAIN_URL_PREFIX,
            TRAIN_DEEPLINK_PREFIX,
            id='train_moscow_kazan',
        ),
        pytest.param(
            f'Поезд Москва — Екатеринбург {_date_str(7)}, 2 пассажира',
            TRAIN_URL_PREFIX,
            TRAIN_DEEPLINK_PREFIX,
            id='train_moscow_ekb',
        ),
    ]


TRANSPORT_QUERIES = _make_queries()


def _find_final_response(response_json: list) -> dict | None:
    """Возвращает финальный объект ответа (isAnswerFinished: true) или None."""
    for item in reversed(response_json):
        if item.get('isAnswerFinished') is True:
            return item
    return None


def _find_link_meta(text_meta_info: list) -> dict | None:
    """Возвращает первый элемент textMetaInfo с type == 'link' или None."""
    for item in text_meta_info:
        if item.get('type') == 'link':
            return item
    return None


@pytest.mark.api
@pytest.mark.parametrize('query, expected_web_prefix, expected_deeplink_prefix', TRANSPORT_QUERIES)
def test_transport_response_has_link_button(
        mock_chat_platform_url,
        query,
        expected_web_prefix,
        expected_deeplink_prefix,
):
    """Проверяет, что ответ на запрос билетов содержит кнопку-ссылку в textMetaInfo.

    Ссылка должна присутствовать в финальном сообщении (isAnswerFinished: true).
    Проверяется структура ссылки: webLinkValue и deepLinkValue начинаются
    с ожидаемых префиксов, startOffset и endOffset — корректные числа.
    """
    chat_id = str(uuid4())
    request_url = f'{mock_chat_platform_url}{MOCK_MESSAGES_ENDPOINT}'
    payload = {
        'chatId': chat_id,
        'messages': [
            {
                'id': str(uuid4()),
                'text': query,
            }
        ],
        'streamingEnabled': False,
        'cardsEnabled': False,
    }

    add_api_request(method='POST', url=request_url, payload=payload)
    response = requests.post(
        request_url,
        json=payload,
        timeout=SYNC_REQUEST_TIMEOUT,
        verify=False,
    )
    add_api_response(response)

    assert response.status_code == 200, (
        f'Ожидался статус 200, получен {response.status_code}.\n'
        f'chatId: {chat_id}\n'
        f'Запрос: {query}\n'
        f'Ответ: {response.text}'
    )

    response_json = response.json()
    assert isinstance(response_json, list) and len(response_json) > 0, (
        f'Ожидался непустой список в ответе.\n'
        f'chatId: {chat_id}\n'
        f'Получено: {response_json}'
    )

    final_response = _find_final_response(response_json)
    assert final_response is not None, (
        f'Не найден финальный ответ (isAnswerFinished: true).\n'
        f'chatId: {chat_id}\n'
        f'Запрос: {query}\n'
        f'Полный ответ: {response_json}'
    )

    messages = final_response.get('messages', [])
    assert len(messages) > 0, (
        f'Финальный ответ не содержит сообщений.\n'
        f'chatId: {chat_id}\n'
        f'Запрос: {query}\n'
        f'Финальный объект: {final_response}'
    )

    text_meta_info = messages[0].get('textMetaInfo', [])
    link_meta = _find_link_meta(text_meta_info)

    assert link_meta is not None, (
        f'Кнопка-ссылка (type: "link") не найдена в textMetaInfo.\n'
        f'=== БАГ-РЕПОРТ ===\n'
        f'chatId: {chat_id}\n'
        f'Запрос: {query}\n'
        f'Текст ответа: {messages[0].get("text", "")!r}\n'
        f'textMetaInfo: {text_meta_info}'
    )

    link_meta_info = link_meta.get('linkMetaInfo', {})
    web_link = link_meta_info.get('webLinkValue', '')
    deep_link = link_meta_info.get('deepLinkValue', '')
    start_offset = link_meta.get('startOffset')
    end_offset = link_meta.get('endOffset')

    assert web_link.startswith(expected_web_prefix), (
        f'webLinkValue не начинается с ожидаемого префикса.\n'
        f'=== БАГ-РЕПОРТ ===\n'
        f'chatId: {chat_id}\n'
        f'Запрос: {query}\n'
        f'Ожидаемый префикс: {expected_web_prefix!r}\n'
        f'Фактический webLinkValue: {web_link!r}'
    )

    assert deep_link.startswith(expected_deeplink_prefix), (
        f'deepLinkValue не начинается с ожидаемого префикса.\n'
        f'=== БАГ-РЕПОРТ ===\n'
        f'chatId: {chat_id}\n'
        f'Запрос: {query}\n'
        f'Ожидаемый префикс: {expected_deeplink_prefix!r}\n'
        f'Фактический deepLinkValue: {deep_link!r}'
    )

    assert isinstance(start_offset, int) and isinstance(end_offset, int), (
        f'startOffset и endOffset должны быть целыми числами.\n'
        f'chatId: {chat_id}\n'
        f'startOffset: {start_offset}, endOffset: {end_offset}'
    )

    assert end_offset > start_offset, (
        f'endOffset должен быть больше startOffset.\n'
        f'chatId: {chat_id}\n'
        f'startOffset: {start_offset}, endOffset: {end_offset}'
    )
