"""Тесты проверки transferSignal при саппортовых запросах.

Проверяет, что при запросах, которые должны переводиться в поддержку,
ответ API содержит "transferSignal": true.
"""

from uuid import uuid4

import pytest
import requests
import urllib3

from utils.attach import add_api_request, add_api_response

MOCK_MESSAGES_ENDPOINT = '/sync/messages'
SYNC_REQUEST_TIMEOUT = 120

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SUPPORT_QUERIES = [
    pytest.param(
        'Я хочу говорить с человеком',
        id='want_human',
    ),
    pytest.param(
        'Отключить уведомления',
        id='disable_notifications',
    ),
    pytest.param(
        'Как потратить баллы?',
        id='spend_points',
    ),
    pytest.param(
        'Как получить справку о поездке?',
        id='travel_certificate',
    ),
    pytest.param(
        'Что можно взять в багаж и ручную кладь?',
        id='baggage_rules',
    ),
    pytest.param(
        'Оставить отзыв',
        id='leave_review',
    ),
    pytest.param(
        'Приложение крашится при попытке купить билет',
        id='app_crash',
    ),
]


@pytest.mark.api
@pytest.mark.parametrize('query', SUPPORT_QUERIES)
def test_support_request_sets_transfer_signal(mock_chat_platform_url, query):
    """Проверяет, что саппортовый запрос возвращает transferSignal: true.

    transferSignal: true означает, что ассистент передаёт чат оператору поддержки.
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

    transfer_signal = response_json[0].get('transferSignal')

    assert transfer_signal is True, (
        f'Ожидался transferSignal: true для саппортового запроса, получено: {transfer_signal}.\n'
        f'=== БАГ-РЕПОРТ ===\n'
        f'chatId: {chat_id}\n'
        f'Запрос: {query}\n'
        f'Полный ответ: {response_json[0]}'
    )
