import json
import unittest
import os

CURRENT_DIR = os.path.dirname(__file__)
FIXTURES_PATH = os.path.join(CURRENT_DIR, 'fixtures')


def get_fixture(file_name: str) -> bytes or dict:
    extension = file_name.split('.')[-1]

    with open(os.path.join(FIXTURES_PATH, file_name), encoding='utf8') as fp:
        body = fp.read().encode()
        if extension == 'json':
            return json.loads(body)
        return body.decode()
