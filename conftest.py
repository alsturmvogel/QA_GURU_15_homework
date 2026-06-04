import os
from pathlib import Path

import allure
import pytest
import requests
from allure_commons.types import AttachmentType
from appium import webdriver as appium_webdriver
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config import BrowserStackConfig, DeviceConfig, get_browserstack_credentials, get_mobile_options
from utils import attach


def pytest_addoption(parser):
    parser.addoption('--base_url', default='https://www.tutu.ru')
    parser.addoption('--remote_url', default='')
    parser.addoption('--browser_name', default='chrome')
    parser.addoption('--browser_version', default='')
    parser.addoption('--headless', default='false')
    parser.addoption('--window_width', default='1920')
    parser.addoption('--window_height', default='1080')
    parser.addoption('--mobile_context', default='browserstack')


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='session')
def mobile_context(request):
    return request.config.getoption('--mobile_context')


@pytest.fixture(scope='session')
def mobile_env_file(mobile_context):
    env_map = {
        'browserstack': '.env.mobile.browserstack',
        'local_real_device': '.env.mobile.local_real_device',
    }

    try:
        return env_map[mobile_context]
    except KeyError as error:
        raise ValueError(
            f'Unsupported mobile context: {mobile_context}. '
            'Use one of: browserstack, local_real_device'
        ) from error


@pytest.fixture(scope='session')
def mock_chat_platform_url():
    return 'https://stepanenko-mock-chat-platform.tutu.rc.rus.tutu.pro'


@pytest.fixture(scope='function')
def appium_driver(load_env, mobile_context, mobile_env_file):
    load_dotenv(mobile_env_file, override=True)
    options, remote_url = get_mobile_options(mobile_context)

    driver = appium_webdriver.Remote(
        command_executor=remote_url,
        options=options,
    )
    driver.implicitly_wait(DeviceConfig.implicit_wait)

    yield driver

    session_id = driver.session_id
    driver.quit()

    if mobile_context != 'browserstack':
        return

    username, access_key = get_browserstack_credentials()

    try:
        response = requests.get(
            BrowserStackConfig.api_url.format(session_id=session_id),
            auth=(username, access_key),
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
