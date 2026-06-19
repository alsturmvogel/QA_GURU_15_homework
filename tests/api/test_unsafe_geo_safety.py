"""Тесты безопасности: проверка блокировки запросов про запрещённые страны и регионы.

Отправляет запросы с упоминанием запрещённых локаций (из UNSAFE_GEO_NAMES в geo.py)
на mock-эндпоинт и проверяет, что ассистент отвечает стандартной фразой отказа.
"""

import pytest
import urllib3

from config import ApiConfig
from tests.api.sync_api_helper import (
    get_final_response_item,
    get_first_message_text,
    parse_sync_response_json,
    send_sync_message,
)
from tests.api.test_data.unsafe_geo_cases import (
    UNSAFE_GEO_QUERIES,
    UNSAFE_GEO_REFUSAL_TEXT,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@pytest.mark.api
@pytest.mark.parametrize('query', UNSAFE_GEO_QUERIES)
def test_unsafe_geo_returns_refusal(mock_chat_platform_url, query):
    """Проверяет, что запросы про запрещённые локации получают стандартный ответ-отказ.

    Отправляет запрос на mock-платформу, которая синхронно проксирует его
    к ассистенту и возвращает ответ. Проверяет, что текст ответа содержит
    стандартную фразу отказа для запрещённых локаций.
    """
    response, chat_id = send_sync_message(
        mock_chat_platform_url=mock_chat_platform_url,
        text=query,
        timeout=ApiConfig.default_sync_request_timeout,
    )
    response_json = parse_sync_response_json(response, chat_id, query)
    final_response_item = get_final_response_item(response_json, chat_id)
    answer_text = get_first_message_text(final_response_item, chat_id)
    assert answer_text == UNSAFE_GEO_REFUSAL_TEXT, (
        f'Ожидался ответ-отказ для запрещённой локации.\n'
        f'Запрос: {query}\n'
        f'Ожидаемый текст: {UNSAFE_GEO_REFUSAL_TEXT!r}\n'
        f'Фактический текст: {answer_text!r}'
    )
