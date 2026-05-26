import json
import urllib3
from pathlib import Path
from uuid import uuid4

import requests
from jsonschema import validate
import pytest


SCHEMA_PATH = Path(__file__).parent.parent / 'resources' / 'schemas' / 'sync_messages_response.schema.json'
SYNC_MESSAGES_ENDPOINT = '/sync/messages'
SYNC_REQUEST_TIMEOUT = 30

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@pytest.mark.api
def test_sync_messages_response_matches_schema(mock_chat_platform_url):
    schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))

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

    response = requests.post(
        f'{mock_chat_platform_url}{SYNC_MESSAGES_ENDPOINT}',
        json=payload,
        timeout=SYNC_REQUEST_TIMEOUT,
        verify=False,
    )

    assert response.status_code == 200, response.text

    response_json = response.json()
    validate(instance=response_json, schema=schema)