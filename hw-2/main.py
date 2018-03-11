from os import getcwd
from os.path import join

import requests

from utils.file_utils import JSONS_DIRECTORY, CREATE_ANALYZER_JSON, read_json_to_string

HOST = r'http://localhost:9200'
ANALYZER = HOST + r'/nlp_analyzer'


def main():
    create_analyzer()


def create_analyzer() -> int:
    json_path = join(getcwd(), JSONS_DIRECTORY, CREATE_ANALYZER_JSON)
    data = read_json_to_string(json_path)
    headers = {'content-type': 'application/json'}
    response = requests.put(url=ANALYZER, headers=headers, data=data)
    return response.status_code


if __name__ == '__main__':
    main()
