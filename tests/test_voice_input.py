from pages.chat_widget import ChatWidget
from pages.main_page import MainPage


def test_user_can_start_voice_recording():
    main_page = MainPage()
    chat_widget = ChatWidget()

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.start_voice_recording()
    chat_widget.should_have_voice_recording_started()
