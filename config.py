import os
from pathlib import Path

from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

load_dotenv()


class ApiConfig:
    sync_messages_endpoint: str = '/sync/messages'
    default_sync_request_timeout: int = 60
    extended_sync_request_timeout: int = 120
    schema_sync_request_timeout: int = 30


class BrowserStackSessionConfig:
    project_name: str = 'QA GURU 15 Homework'
    build_name: str = 'Jarvel Mobile Tests'
    session_name: str = 'Jarvel Android Test'
    debug: bool = True
    network_logs: bool = True


class DeviceConfig:
    implicit_wait: int = 20
    automation_name: str = 'UiAutomator2'


class BrowserStackConfig:
    credentials_env_file: str = '.env.mobile.browserstack.credentials'
    hub_url: str = 'https://hub.browserstack.com/wd/hub'
    api_url: str = 'https://api-cloud.browserstack.com/app-automate/sessions/{session_id}.json'


def _load_browserstack_credentials() -> tuple[str, str]:
    load_dotenv(BrowserStackConfig.credentials_env_file, override=True)
    return (
        os.getenv('BROWSERSTACK_USERNAME', ''),
        os.getenv('BROWSERSTACK_ACCESS_KEY', ''),
    )


def _resolve_local_app_path(app_path: str) -> str:
    path = Path(app_path)
    if path.is_absolute():
        return str(path)
    return str((Path(__file__).resolve().parent / path).resolve())


def get_mobile_options(mobile_context: str) -> tuple[UiAutomator2Options, str]:
    options = UiAutomator2Options()

    if mobile_context == 'browserstack':
        username, access_key = _load_browserstack_credentials()
        app = os.getenv('APP', '')
        remote_url = os.getenv('REMOTE_URL', BrowserStackConfig.hub_url)
        device_name = os.getenv('DEVICE_NAME', 'Samsung Galaxy S22')
        platform_name = os.getenv('PLATFORM_NAME', 'Android')
        platform_version = os.getenv('PLATFORM_VERSION', '12.0')

        if not username or not access_key:
            raise ValueError(
                'Для запуска mobile-тестов через BrowserStack необходимо указать '
                'BROWSERSTACK_USERNAME и BROWSERSTACK_ACCESS_KEY '
                f'в {BrowserStackConfig.credentials_env_file}'
            )

        if not app:
            raise ValueError(
                'Для запуска mobile-тестов через BrowserStack необходимо указать '
                'APP в .env.mobile.browserstack (например: bs://abc123...)'
            )

        options.set_capability('platformName', platform_name)
        options.set_capability('deviceName', device_name)
        options.set_capability('platformVersion', platform_version)
        options.set_capability('app', app)
        options.set_capability('automationName', DeviceConfig.automation_name)
        options.set_capability('bstack:options', {
            'userName': username,
            'accessKey': access_key,
            'projectName': BrowserStackSessionConfig.project_name,
            'buildName': BrowserStackSessionConfig.build_name,
            'sessionName': BrowserStackSessionConfig.session_name,
            'debug': BrowserStackSessionConfig.debug,
            'networkLogs': BrowserStackSessionConfig.network_logs,
        })
        return options, remote_url

    if mobile_context == 'local_real_device':
        remote_url = os.getenv('REMOTE_URL', 'http://127.0.0.1:4723')
        device_name = os.getenv('DEVICE_NAME', '')
        app = os.getenv('APP', '')
        platform_name = os.getenv('PLATFORM_NAME', 'Android')
        automation_name = os.getenv('AUTOMATION_NAME', DeviceConfig.automation_name)
        udid = os.getenv('UDID', '')

        if not device_name:
            raise ValueError(
                'Для локального запуска mobile-тестов необходимо указать DEVICE_NAME '
                'в .env.mobile.local_real_device'
            )

        if not app:
            raise ValueError(
                'Для локального запуска mobile-тестов необходимо указать APP '
                'в .env.mobile.local_real_device'
            )

        options.set_capability('platformName', platform_name)
        options.set_capability('deviceName', device_name)
        options.set_capability('automationName', automation_name)
        options.set_capability('app', _resolve_local_app_path(app))
        options.set_capability('newCommandTimeout', 240)
        options.set_capability('adbExecTimeout', 120000)
        options.set_capability('uiautomator2ServerInstallTimeout', 120000)
        options.set_capability('androidInstallTimeout', 120000)
        options.set_capability('autoGrantPermissions', True)

        if udid:
            options.set_capability('udid', udid)

        return options, remote_url

    raise ValueError(
        f'Unsupported mobile context: {mobile_context}. '
        'Use one of: browserstack, local_real_device'
    )


def get_browserstack_credentials() -> tuple[str, str]:
    return _load_browserstack_credentials()
