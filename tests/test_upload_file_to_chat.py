from pathlib import Path

from pages.main_page import MainPage
from pages.chat_widget import ChatWidget


def test_user_can_upload_file_to_chat():
    main_page = MainPage()
    chat_widget = ChatWidget()

    file_path = str(Path(__file__).parent.parent / 'resources' / 'test_file.docx')

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.upload_file_to_chat(file_path)
    chat_widget.should_have_reply_after_file_upload()