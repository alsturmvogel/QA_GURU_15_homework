"""Тесты проверки transferSignal при саппортовых запросах.

Проверяет, что при запросах, которые должны переводиться в поддержку,
ответ API содержит "transferSignal": true.
"""

import pytest
import urllib3

from config import ApiConfig
from tests.api.sync_api_helper import (
    get_final_response_item,
    parse_sync_response_json,
    send_sync_message,
)
from tests.api.test_data.support_transfer_cases import SUPPORT_QUERIES

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@pytest.mark.api
@pytest.mark.parametrize('query', SUPPORT_QUERIES)
def test_support_request_sets_transfer_signal(mock_chat_platform_url, query):
    """Проверяет, что саппортовый запрос возвращает transferSignal: true.

    transferSignal: true означает, что ассистент передаёт чат оператору поддержки.
    """
    response, chat_id = send_sync_message(
        mock_chat_platform_url=mock_chat_platform_url,
        text=query,
        timeout=ApiConfig.extended_sync_request_timeout,
    )
    response_json = parse_sync_response_json(response, chat_id, query)
    final_response_item = get_final_response_item(response_json, chat_id)

    transfer_signal = final_response_item.get('transferSignal')

    assert transfer_signal is True, (
        f'Ожидался transferSignal: true для саппортового запроса, получено: {transfer_signal}.\n'
        f'=== БАГ-РЕПОРТ ===\n'
        f'chatId: {chat_id}\n'
        f'Запрос: {query}\n'
        f'Полный ответ: {final_response_item}'
    )
