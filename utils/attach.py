import json
import logging

import allure
from allure_commons.types import AttachmentType

api_logger = logging.getLogger('api_tests')


def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(
        body=png,
        name='screenshot',
        attachment_type=AttachmentType.PNG,
        extension='.png'
    )


def add_logs(browser):
    log = ''.join(f'{text}\n' for text in browser.driver.get_log('browser'))
    allure.attach(
        log,
        'browser_logs',
        AttachmentType.TEXT,
        '.log'
    )


def add_html(browser):
    html = browser.driver.page_source
    allure.attach(
        html,
        'page_source',
        AttachmentType.HTML,
        '.html'
    )


def _to_pretty_json(data):
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def add_api_request(method, url, payload=None, headers=None):
    request_data = {
        'method': method,
        'url': url,
        'headers': headers or {},
        'payload': payload,
    }
    api_logger.info('api_request method=%s client_url=%s', method, url)
    allure.attach(
        _to_pretty_json(request_data),
        'api_request',
        AttachmentType.JSON,
        '.json'
    )


def add_api_response(response):
    try:
        response_body = response.json()
    except ValueError:
        response_body = response.text

    response_data = {
        'status_code': response.status_code,
        'url': response.url,
        'body': response_body,
    }
    api_logger.info(
        'api_response status_code=%s client_url=%s',
        response.status_code,
        response.url,
    )
    allure.attach(
        _to_pretty_json(response_data),
        'api_response',
        AttachmentType.JSON,
        '.json'
    )
