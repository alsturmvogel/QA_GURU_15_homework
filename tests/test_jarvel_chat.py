from pathlib import Path

from pages.chat_widget import ChatWidget
from pages.main_page import MainPage


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

    file_path = Path(__file__).parent.parent / 'resources' / 'test_file.docx'
    assert file_path.exists(), f'Файл не найден: {file_path}'

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.upload_file_to_chat(str(file_path))
    chat_widget.should_have_reply_after_file_upload()