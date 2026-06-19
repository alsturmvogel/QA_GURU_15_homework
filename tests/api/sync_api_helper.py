from uuid import uuid4

import requests

from config import ApiConfig
from utils.attach import add_api_request, add_api_response


def send_sync_message(
        mock_chat_platform_url: str,
        text: str,
        timeout: int | float,
        chat_id: str | None = None,
) -> tuple[requests.Response, str]:
    """Отправляет sync-запрос в mock chat platform и возвращает response и chat_id."""
    actual_chat_id = chat_id or str(uuid4())
    request_url = f'{mock_chat_platform_url}{ApiConfig.sync_messages_endpoint}'
    payload = {
        'chatId': actual_chat_id,
        'messages': [
            {
                'id': str(uuid4()),
                'text': text,
            }
        ],
        'streamingEnabled': False,
        'cardsEnabled': False,
    }

    add_api_request(method='POST', url=request_url, payload=payload)
    response = requests.post(
        request_url,
        json=payload,
        timeout=timeout,
        verify=False,
    )
    add_api_response(response)

    return response, actual_chat_id


def parse_sync_response_json(response: requests.Response, chat_id: str, query: str) -> list:
    """Проверяет базовую успешность sync-ответа и возвращает response.json()."""
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

    return response_json


def get_final_response_item(response_json: list, chat_id: str) -> dict:
    """Возвращает финальный элемент sync-ответа.

    Предпочитает последний элемент с isAnswerFinished=True.
    Если такого нет, возвращает последний элемент списка.
    """
    assert len(response_json) > 0, (
        f'Ожидался непустой список в ответе.\n'
        f'chatId: {chat_id}\n'
        f'Получено: {response_json}'
    )

    finished_items = [item for item in response_json if item.get('isAnswerFinished') is True]
    if finished_items:
        return finished_items[-1]

    return response_json[-1]


def get_first_message_text(response_item: dict, chat_id: str) -> str:
    """Возвращает текст первого сообщения из элемента sync-ответа."""
    messages = response_item.get('messages', [])
    assert len(messages) > 0, (
        f'Ожидались сообщения в ответе.\n'
        f'chatId: {chat_id}\n'
        f'Получено: {response_item}'
    )

    return messages[0].get('text', '')
