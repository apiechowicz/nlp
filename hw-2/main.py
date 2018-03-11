from os import getcwd

import requests

from utils.file_utils import get_create_analyzer_json, get_create_index_json

HOST = r'http://localhost:9200'
ANALYZER = HOST + r'/nlp_analyzer'
INDEX = HOST + r'/nlp_index'


def main():
    create_analyzer()
    create_index()


def create_analyzer() -> int:
    data = get_create_analyzer_json(getcwd())
    headers = {'content-type': 'application/json'}
    response = requests.put(url=ANALYZER, headers=headers, data=data)
    return response.status_code


def create_index() -> int:
    data = get_create_index_json(getcwd())
    headers = {'content-type': 'application/json'}
    response = requests.put(url=INDEX, headers=headers, data=data)
    return response.status_code


if __name__ == '__main__':
    main()
