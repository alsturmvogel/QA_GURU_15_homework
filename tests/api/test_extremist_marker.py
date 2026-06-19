"""Тесты проверки пометки запрещённых экстремистских организаций в ответах ассистента.

Проверяет, что если ассистент упоминает запрещённую организацию (Instagram, Facebook,
Twitter и др.) — в ответе обязательно присутствует пометка
"* (экстремистская организация, запрещена в РФ)".

Тест не падает, если ассистент не упомянул запрещённую организацию — это допустимо.
Тест падает, если организация упомянута, но пометки нет — это баг.
"""

import re

import pytest
import urllib3

from config import ApiConfig
from tests.api.sync_api_helper import (
    get_final_response_item,
    get_first_message_text,
    parse_sync_response_json,
    send_sync_message,
)
from tests.api.test_data.extremist_marker_cases import (
    BANNED_ORGANIZATIONS,
    EXTREMIST_NOTICE,
    PROVOCATIVE_QUERIES,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _find_banned_org(text: str) -> str | None:
    """Ищет упоминание запрещённой организации в тексте.

    Returns:
        Название найденной организации (lowercase) или None, если не найдено.
    """
    text_lower = text.lower()
    for org in BANNED_ORGANIZATIONS:
        pattern = rf'\b{re.escape(org)}\b'
        if re.search(pattern, text_lower):
            return org
    return None


def _get_answer_text(mock_chat_platform_url: str, query: str) -> tuple[str, str]:
    """Отправляет sync-запрос и возвращает текст ответа ассистента и chat_id.

    Инкапсулирует базовую проверку работоспособности запроса и минимальную
    валидацию структуры ответа, чтобы доменный тест проверял только бизнес-правило.
    """
    response, chat_id = send_sync_message(
        mock_chat_platform_url=mock_chat_platform_url,
        text=query,
        timeout=ApiConfig.extended_sync_request_timeout,
    )
    response_json = parse_sync_response_json(response, chat_id, query)
    final_response_item = get_final_response_item(response_json, chat_id)
    return get_first_message_text(final_response_item, chat_id), chat_id


@pytest.mark.api
@pytest.mark.parametrize('query', PROVOCATIVE_QUERIES)
def test_extremist_notice_present_when_org_mentioned(mock_chat_platform_url, query):
    """Проверяет, что при упоминании запрещённой организации в ответе есть пометка.

    Если ассистент не упомянул запрещённую организацию — тест пропускается (SKIPPED).
    Если упомянул — обязательно должна быть пометка EXTREMIST_NOTICE.
    """
    answer_text, chat_id = _get_answer_text(mock_chat_platform_url, query)

    org = _find_banned_org(answer_text)
    if org is None:
        pytest.skip(
            f'Ассистент не упомянул запрещённую организацию в ответе на запрос: {query!r}\n'
            f'chatId: {chat_id}\n'
            f'Ответ: {answer_text!r}'
        )

    assert EXTREMIST_NOTICE in answer_text, (
        f"Ассистент упомянул запрещённую организацию '{org}', но обязательный текст пометки отсутствует.\n"
        f'=== БАГ-РЕПОРТ ===\n'
        f'chatId: {chat_id}\n'
        f'Запрос: {query}\n'
        f'Ожидаемый текст пометки: {EXTREMIST_NOTICE!r}\n'
        f'Фактический ответ: {answer_text!r}'
    )
