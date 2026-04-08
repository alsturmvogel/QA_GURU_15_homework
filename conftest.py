import pytest
from selene import browser
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function", autouse=True)
def browser_management():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")

    browser.config.base_url = "https://www.tutu.ru"
    browser.config.timeout = 20
    browser.config.driver_options = options

    yield

    browser.quit()