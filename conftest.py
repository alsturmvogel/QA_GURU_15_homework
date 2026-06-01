import os
from pathlib import Path

import allure
import pytest
import requests
from allure_commons.types import AttachmentType
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options
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


@pytest.fixture(scope='session')
def mock_chat_platform_url():
    return 'https://stepanenko-mock-chat-platform.tutu.rc.rus.tutu.pro'


@pytest.fixture(scope='function')
def appium_driver(load_env):
    bs_username = os.getenv('BROWSERSTACK_USERNAME')
    bs_access_key = os.getenv('BROWSERSTACK_ACCESS_KEY')

    if not bs_username or not bs_access_key:
        raise ValueError(
            'Для запуска мобильных тестов необходимо указать '
            'BROWSERSTACK_USERNAME и BROWSERSTACK_ACCESS_KEY в .env'
        )

    app_url = os.getenv('BROWSERSTACK_APP_URL')
    if not app_url:
        raise ValueError(
            'Для запуска мобильных тестов необходимо указать '
            'BROWSERSTACK_APP_URL в .env (например: bs://abc123...)'
        )

    options = UiAutomator2Options()
    options.set_capability('platformName', 'android')
    options.set_capability('deviceName', 'Samsung Galaxy S22')
    options.set_capability('platformVersion', '12.0')
    options.set_capability('app', app_url)
    options.set_capability('automationName', 'UiAutomator2')
    options.set_capability('bstack:options', {
        'userName': bs_username,
        'accessKey': bs_access_key,
        'projectName': 'QA GURU 15 Homework',
        'buildName': 'Jarvel Mobile Tests',
        'sessionName': 'Jarvel Android Test',
        'debug': True,
        'networkLogs': True,
    })

    driver = appium_webdriver.Remote(
        command_executor='https://hub.browserstack.com/wd/hub',
        options=options,
    )
    driver.implicitly_wait(20)

    yield driver

    # Прикрепить видео сессии из BrowserStack к Allure-отчёту
    session_id = driver.session_id
    driver.quit()

    try:
        response = requests.get(
            f'https://api-cloud.browserstack.com/app-automate/sessions/{session_id}.json',
            auth=(bs_username, bs_access_key),
            timeout=15,
        )
        video_url = response.json().get('automation_session', {}).get('video_url')
        if video_url:
            video_response = requests.get(video_url, timeout=60)
            allure.attach(
                video_response.content,
                name='BrowserStack Video',
                attachment_type=AttachmentType.MP4,
                extension='.mp4',
            )
    except Exception:
        pass  # Не прерываем тест из-за ошибки прикрепления видео


@pytest.fixture(scope='function', autouse=True)
def browser_management(request):
    if request.node.get_closest_marker('api'):
        yield
        return

    if request.node.get_closest_marker('mobile'):
        yield
        return

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
