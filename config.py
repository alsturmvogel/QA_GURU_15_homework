import os

from dotenv import load_dotenv

load_dotenv()


class BrowserStackConfig:
    username: str = os.getenv('BROWSERSTACK_USERNAME', '')
    access_key: str = os.getenv('BROWSERSTACK_ACCESS_KEY', '')
    app_url: str = os.getenv('BROWSERSTACK_APP_URL', '')
    hub_url: str = 'https://hub.browserstack.com/wd/hub'
    api_url: str = 'https://api-cloud.browserstack.com/app-automate/sessions/{session_id}.json'


class DeviceConfig:
    platform_name: str = 'android'
    device_name: str = 'Samsung Galaxy S22'
    platform_version: str = '12.0'
    automation_name: str = 'UiAutomator2'
    implicit_wait: int = 20


class BrowserStackSessionConfig:
    project_name: str = 'QA GURU 15 Homework'
    build_name: str = 'Jarvel Mobile Tests'
    session_name: str = 'Jarvel Android Test'
    debug: bool = True
    network_logs: bool = True
