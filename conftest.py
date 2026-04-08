import os
import pytest
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function", autouse=True)
def browser_management():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")

    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASSWORD")
    selenoid_url = os.getenv("SELENOID_URL")

    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "127.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }

    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options
    )

    browser.config.driver = driver
    browser.config.base_url = "https://www.tutu.ru"
    browser.config.timeout = 20

    yield

    driver.quit()