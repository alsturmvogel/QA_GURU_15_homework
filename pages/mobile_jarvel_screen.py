import time

import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MobileJarvelScreen:
    CLOSE_BANNER_BUTTON = (
        AppiumBy.XPATH,
        "//*[@content-desc='Закрыть']",
    )
    JARVEL_NAV_BUTTON = (
        AppiumBy.XPATH,
        "//*[@resource-id='ru.tutu.tutu_emp:id/navigation_jarvel']",
    )
    JARVEL_NAV_BUTTON_BY_TEXT = (
        AppiumBy.XPATH,
        "//*[@text='Джарвел' or @content-desc='Джарвел']",
    )
    JARVEL_NAV_BUTTON_BY_ACCESSIBILITY_ID = (
        AppiumBy.ACCESSIBILITY_ID,
        'Джарвел',
    )
    START_SCREEN_READY_MARKERS = [
        (
            AppiumBy.XPATH,
            "//*[@resource-id='ru.tutu.tutu_emp:id/navigation_jarvel']",
        ),
        (
            AppiumBy.XPATH,
            "//*[@text='Джарвел' or @content-desc='Джарвел']",
        ),
        (
            AppiumBy.XPATH,
            "//*[@content-desc='Закрыть']",
        ),
    ]
    WELCOME_MESSAGE = (
        AppiumBy.XPATH,
        "//android.widget.TextView[contains(@text,'Привет! Я Джарвел — умный помощник от Туту.')]",
    )
    YOUR_TRIP_SECTION = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Ваша поездка']",
    )
    SHOW_BUTTON = (
        AppiumBy.XPATH,
        "//android.widget.Button[@text='Показать']",
    )
    EMPTY_TRIP_TITLE = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Пока тут пусто']",
    )
    EMPTY_TRIP_DESCRIPTION = (
        AppiumBy.XPATH,
        "//android.widget.TextView[contains(@text,'Попросите Джарвела подобрать отель')]",
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.short_wait = WebDriverWait(driver, 5)

    def dismiss_banner_if_present(self):
        """Закрыть баннер-опрос, если он появился при запуске приложения."""
        with allure.step('Закрыть баннер-опрос (если отображается)'):
            try:
                close_btn = self.short_wait.until(
                    EC.presence_of_element_located(self.CLOSE_BANNER_BUTTON)
                )
                # Нажимаем на родительский кликабельный элемент
                parent = self.driver.find_element(
                    AppiumBy.XPATH,
                    "//android.view.View[@clickable='true' and .//*[@content-desc='Закрыть']]",
                )
                parent.click()
            except TimeoutException:
                pass  # Баннер не появился — продолжаем
        return self

    def wait_for_start_screen(self):
        with allure.step('Дождаться готовности стартового экрана приложения'):
            markers = self.START_SCREEN_READY_MARKERS
            last_exception = None

            for _ in range(3):
                for locator in markers:
                    try:
                        self.short_wait.until(
                            EC.presence_of_element_located(locator)
                        )
                        return self
                    except TimeoutException as error:
                        last_exception = error
                time.sleep(2)

            raise TimeoutException(
                'Стартовый экран приложения не успел прогрузиться'
            ) from last_exception

    def open_jarvel_chat(self):
        with allure.step('Закрыть баннер и открыть чат Джарвела'):
            self.wait_for_start_screen()
            self.dismiss_banner_if_present()

        with allure.step('Нажать на кнопку "Джарвел" в нижней навигации'):
            jarvel_locators = [
                self.JARVEL_NAV_BUTTON,
                self.JARVEL_NAV_BUTTON_BY_TEXT,
                self.JARVEL_NAV_BUTTON_BY_ACCESSIBILITY_ID,
            ]

            last_exception = None

            for _ in range(2):
                for locator in jarvel_locators:
                    try:
                        element = self.wait.until(
                            EC.element_to_be_clickable(locator)
                        )
                        element.click()
                        return self
                    except TimeoutException as error:
                        last_exception = error
                time.sleep(2)

            raise TimeoutException(
                'Не удалось найти или нажать кнопку "Джарвел" ни по одному из локаторов'
            ) from last_exception
        return self

    def should_have_welcome_message(self):
        with allure.step('Проверить приветственное сообщение Джарвела'):
            element = self.wait.until(
                EC.visibility_of_element_located(self.WELCOME_MESSAGE)
            )
            assert element.is_displayed(), (
                'Приветственное сообщение Джарвела не отображается'
            )
        return self

    def should_have_your_trip_section(self):
        with allure.step('Проверить наличие раздела "Ваша поездка"'):
            element = self.wait.until(
                EC.visibility_of_element_located(self.YOUR_TRIP_SECTION)
            )
            assert element.is_displayed(), (
                'Раздел "Ваша поездка" не отображается'
            )
        return self

    def tap_show_button(self):
        with allure.step('Нажать кнопку "Показать"'):
            self.wait.until(
                EC.element_to_be_clickable(self.SHOW_BUTTON)
            ).click()
        return self

    def should_have_empty_trip_state(self):
        with allure.step('Проверить заголовок пустого состояния "Пока тут пусто"'):
            title = self.wait.until(
                EC.visibility_of_element_located(self.EMPTY_TRIP_TITLE)
            )
            assert title.is_displayed(), (
                'Текст "Пока тут пусто" не отображается'
            )

        with allure.step('Проверить описание пустого состояния "Попросите Джарвела..."'):
            description = self.wait.until(
                EC.visibility_of_element_located(self.EMPTY_TRIP_DESCRIPTION)
            )
            assert description.is_displayed(), (
                'Текст "Попросите Джарвела подобрать отель..." не отображается'
            )
        return self
