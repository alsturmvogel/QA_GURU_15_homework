import json
import urllib3
from pathlib import Path
from uuid import uuid4

import requests
from jsonschema import validate
import pytest

from utils.attach import add_api_request, add_api_response


SCHEMA_PATH = Path(__file__).parent.parent.parent / 'resources' / 'schemas' / 'sync_messages_response.schema.json'
SYNC_MESSAGES_ENDPOINT = '/sync/messages'
SYNC_REQUEST_TIMEOUT = 30

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@pytest.mark.api
def test_sync_messages_response_matches_schema(mock_chat_platform_url):
    schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    request_url = f'{mock_chat_platform_url}{SYNC_MESSAGES_ENDPOINT}'

    payload = {
        'chatId': 'eeeeeeee-eeee-eeee-eeee-eeeeeeee1010',
        'messages': [
            {
                'id': str(uuid4()),
                'text': 'Привет'
            }
        ],
        'streamingEnabled': False,
        'cardsEnabled': False
    }

    add_api_request(method='POST', url=request_url, payload=payload)
    response = requests.post(
        request_url,
        json=payload,
        timeout=SYNC_REQUEST_TIMEOUT,
        verify=False,
    )
    add_api_response(response)

    assert response.status_code == 200, response.text

    response_json = response.json()
    validate(instance=response_json, schema=schema)