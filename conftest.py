import os

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils import attach


def pytest_addoption(parser):
    parser.addoption('--base_url', default='https://www.tutu.ru')
    parser.addoption('--remote_url', default='')
    parser.addoption('--browser_name', default='chrome')
    parser.addoption('--browser_version', default='')
    parser.addoption('--headless', default='false')
    parser.addoption('--window_width', default='1920')
    parser.addoption('--window_height', default='1080')


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def browser_management(request):
    base_url = request.config.getoption('--base_url')
    remote_url = request.config.getoption('--remote_url')
    browser_name = request.config.getoption('--browser_name')
    browser_version = request.config.getoption('--browser_version')
    headless = request.config.getoption('--headless').lower() == 'true'
    window_width = request.config.getoption('--window_width')
    window_height = request.config.getoption('--window_height')

    selenoid_login = os.getenv('SELENOID_LOGIN')
    selenoid_password = os.getenv('SELENOID_PASSWORD')

    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_argument(f'--window-size={window_width},{window_height}')
        options.add_argument('--use-fake-ui-for-media-stream')
        options.add_argument('--use-fake-device-for-media-stream')

        if headless:
            options.add_argument('--headless=new')

        if remote_url:
            options.set_capability('browserName', 'chrome')
            if browser_version:
                options.set_capability('browserVersion', browser_version)
            options.set_capability('selenoid:options', {
                'enableVNC': True,
                'enableVideo': False
            })

    elif browser_name == 'firefox':
        options = FirefoxOptions()

        if headless:
            options.add_argument('-headless')

        if remote_url:
            options.set_capability('browserName', 'firefox')
            if browser_version:
                options.set_capability('browserVersion', browser_version)
            options.set_capability('selenoid:options', {
                'enableVNC': True,
                'enableVideo': False
            })

    else:
        raise ValueError(f'Unsupported browser: {browser_name}')

    if remote_url:
        if not selenoid_login or not selenoid_password:
            raise ValueError(
                'Для удаленного запуска необходимо указать '
                'SELENOID_LOGIN и SELENOID_PASSWORD в .env'
            )

        driver = webdriver.Remote(
            command_executor=f'https://{selenoid_login}:{selenoid_password}@{remote_url}/wd/hub',
            options=options
        )
    else:
        if browser_name == 'chrome':
            driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Firefox(options=options)

    browser.config.driver = driver
    browser.config.base_url = base_url
    browser.config.timeout = 20

    driver.set_window_size(int(window_width), int(window_height))

    yield

    attach.add_screenshot(browser)
    attach.add_html(browser)

    if remote_url:
        attach.add_logs(browser)
        # attach.add_video()

    driver.quit()
