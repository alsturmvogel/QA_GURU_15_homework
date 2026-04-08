import allure
from selene import browser, be


class MainPage:
    def open(self):
        with allure.step('Открыть главную страницу tutu.ru'):
            browser.open("/")
        return self

    def open_jarvel_chat(self):
        with allure.step('Нажать на кнопку открытия чата с Джарвелом'):
            browser.element('//button[.//span[text()="Джарвел"]]').should(be.visible).click()
        return self