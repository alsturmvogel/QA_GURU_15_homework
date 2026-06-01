import pytest

from pages.mobile_jarvel_screen import MobileJarvelScreen


@pytest.mark.mobile
def test_jarvel_welcome_message_is_visible(appium_driver):
    """Открытие чата Джарвел и проверка приветственного сообщения.

    Шаги:
    1. Нажать на кнопку "Джарвел" в нижней навигации.
    2. Проверить, что отображается приветственное сообщение:
       "Привет! Я Джарвел — умный помощник от Туту.
        Помогаю спланировать путешествие и найти нужную информацию.
        Со мной можно общаться и уточнять вопросы — я быстро подстраиваюсь."
    """
    screen = MobileJarvelScreen(appium_driver)

    screen.open_jarvel_chat()
    screen.should_have_welcome_message()


@pytest.mark.mobile
def test_your_trip_section_is_visible(appium_driver):
    """Проверка наличия раздела "Ваша поездка" на экране Джарвела.

    Шаги:
    1. Нажать на кнопку "Джарвел" в нижней навигации.
    2. Проверить, что на экране отображается текст "Ваша поездка".
    """
    screen = MobileJarvelScreen(appium_driver)

    screen.open_jarvel_chat()
    screen.should_have_your_trip_section()


@pytest.mark.mobile
def test_show_button_opens_empty_trip_state(appium_driver):
    """Нажатие на кнопку "Показать" и проверка пустого состояния раздела поездок.

    Шаги:
    1. Нажать на кнопку "Джарвел" в нижней навигации.
    2. Нажать кнопку "Показать".
    3. Проверить, что отображается заголовок "Пока тут пусто".
    4. Проверить, что отображается текст
       "Попросите Джарвела подобрать отель или перелёт — выбранное появится здесь..."
    """
    screen = MobileJarvelScreen(appium_driver)

    screen.open_jarvel_chat()
    screen.tap_show_button()
    screen.should_have_empty_trip_state()
