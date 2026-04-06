from pages.main_page import MainPage
from pages.chat_widget import ChatWidget


def test_user_can_type_hello_and_press_enter():
    main_page = MainPage()
    chat_widget = ChatWidget()

    main_page.open()
    main_page.open_jarvel_chat()
    chat_widget.send_hello_message()
    chat_widget.should_have_sent_hello_and_reply()