from pages.chat_widget import ChatWidget
from pages.main_page import MainPage


def test_user_can_see_jarvel_capabilities_texts():
    main_page = MainPage()
    chat_widget = ChatWidget()

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.should_have_capabilities_texts()
