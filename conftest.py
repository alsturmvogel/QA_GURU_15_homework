import pytest
from selene import browser
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function", autouse=True)
def browser_management():
    options = Options()
    browser.driver.set_window_size(1920, 1080)

    browser.config.base_url = "https://www.tutu.ru"
    browser.config.timeout = 8
    browser.config.driver_options = options

    yield

    browser.quit()