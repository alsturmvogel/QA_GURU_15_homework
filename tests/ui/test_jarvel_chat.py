from pathlib import Path
from uuid import uuid4

import allure
import pytest
import requests

from pages.chat_widget import ChatWidget
from pages.main_page import MainPage

from tests.constants import DEFAULT_SYNC_REQUEST_TIMEOUT, SYNC_MESSAGES_ENDPOINT


def test_user_can_see_welcome_message():
    main_page = MainPage()
    chat_widget = ChatWidget()

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.should_have_welcome_message()


def test_user_can_see_jarvel_capabilities_texts():
    main_page = MainPage()
    chat_widget = ChatWidget()

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.should_have_capabilities_texts()


def test_user_can_type_hello_and_press_enter():
    main_page = MainPage()
    chat_widget = ChatWidget()

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.send_hello_message()
    chat_widget.should_have_sent_hello_and_reply()


def test_user_can_start_voice_recording():
    main_page = MainPage()
    chat_widget = ChatWidget()

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.start_voice_recording()
    chat_widget.should_have_voice_recording_started()


def test_user_can_upload_file_to_chat():
    main_page = MainPage()
    chat_widget = ChatWidget()

    file_path = Path(__file__).parent.parent.parent / 'resources' / 'test_file.docx'
    assert file_path.exists(), f'Файл не найден: {file_path}'

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.upload_file_to_chat(str(file_path))
    chat_widget.should_have_reply_after_file_upload()


@allure.title('Ответ ассистента на вопрос "Что ты умеешь делать?" совпадает с ответом API')
def test_jarvel_ui_response_matches_api_response(mock_chat_platform_url):
    """Двухуровневая проверка ответа ассистента на вопрос о его возможностях.

    Шаг 1 (API): Отправляем вопрос на mock-стенд и получаем эталонный ответ.
    Шаг 2 (UI): Открываем чат на tutu.ru, задаём тот же вопрос и проверяем,
    что браузер отображает текст, совпадающий с ответом API.

    Если API вернул ошибку — тест пропускается (проблема на стороне бэкенда).
    Если UI не показывает ожидаемый текст — это баг фронтенда.
    """
    query = 'Что ты умеешь делать?'

    with allure.step(f'[API] Отправить запрос "{query}" на mock-стенд и получить эталонный ответ'):
        payload = {
            'chatId': str(uuid4()),
            'messages': [
                {
                    'id': str(uuid4()),
                    'text': query,
                }
            ],
            'streamingEnabled': False,
            'cardsEnabled': False,
        }

        response = requests.post(
            f'{mock_chat_platform_url}{SYNC_MESSAGES_ENDPOINT}',
            json=payload,
            timeout=DEFAULT_SYNC_REQUEST_TIMEOUT,
            verify=False,
        )

    with allure.step('[API] Проверить, что API вернул статус 200'):
        if response.status_code != 200:
            pytest.skip(
                f'API mock-стенда недоступен (статус {response.status_code}), '
                f'UI-тест не имеет смысла без эталонного ответа.'
            )

    with allure.step('[API] Извлечь текст ответа ассистента'):
        response_json = response.json()
        messages = response_json[0].get('messages', [])
        assert len(messages) > 0, f'API вернул пустой список сообщений: {response_json}'
        expected_text = messages[0].get('text', '')
        assert expected_text, f'API вернул пустой текст ответа: {response_json}'

    main_page = MainPage()
    chat_widget = ChatWidget()

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.send_message(query)
    chat_widget.should_have_reply_containing(expected_text)
