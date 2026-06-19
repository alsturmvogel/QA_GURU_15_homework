import json
from pathlib import Path

import pytest
import urllib3
from jsonschema import validate

from config import ApiConfig
from tests.api.sync_api_helper import send_sync_message

SCHEMA_PATH = Path(__file__).parent.parent.parent / 'resources' / 'schemas' / 'sync_messages_response.schema.json'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@pytest.mark.api
def test_sync_messages_response_matches_schema(mock_chat_platform_url):
    schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    response, _ = send_sync_message(
        mock_chat_platform_url=mock_chat_platform_url,
        text='Привет',
        timeout=ApiConfig.schema_sync_request_timeout,
        chat_id='eeeeeeee-eeee-eeee-eeee-eeeeeeee1010',
    )

    assert response.status_code == 200, response.text

    response_json = response.json()
    validate(instance=response_json, schema=schema)
