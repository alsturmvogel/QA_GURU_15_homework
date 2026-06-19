"""Тесты проверки наличия кнопки-ссылки на поиск билетов в ответе ассистента.

При запросе билетов на автобус или поезд с указанием маршрута, даты и числа пассажиров
ассистент должен вернуть ссылку в поле textMetaInfo финального сообщения.

Используются популярные маршруты с высокой вероятностью наличия рейсов.
Если ссылка не пришла — это баг.
"""

import pytest

from config import ApiConfig
from tests.api.sync_api_helper import parse_sync_response_json, send_sync_message
from tests.api.test_data.transport_link_cases import TRANSPORT_QUERIES


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
    response, chat_id = send_sync_message(
        mock_chat_platform_url=mock_chat_platform_url,
        text=query,
        timeout=ApiConfig.extended_sync_request_timeout,
    )
    response_json = parse_sync_response_json(response, chat_id, query)

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
