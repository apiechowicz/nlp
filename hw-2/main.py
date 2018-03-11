from os import getcwd

import requests

from utils.argument_parser import parse_arguments
from utils.file_utils import get_create_analyzer_json, get_create_index_json, get_files_to_be_processed, \
    extract_and_upload_data

HOST = r'http://localhost:9200'
ANALYZER = HOST + r'/nlp_analyzer'
INDEX = HOST + r'/nlp_index'
INDEX_DATA = INDEX + r'/judgements'
HEADERS = {'content-type': 'application/json'}


def main():
    input_dir, judgement_year = parse_arguments()
    create_analyzer()
    create_index()
    files = get_files_to_be_processed(input_dir)
    for file in files:
        extract_and_upload_data(file, judgement_year, INDEX_DATA, HEADERS)


def create_analyzer() -> int:
    data = get_create_analyzer_json(getcwd())
    response = requests.put(url=ANALYZER, headers=HEADERS, data=data)
    return response.status_code


def create_index() -> int:
    data = get_create_index_json(getcwd())
    response = requests.put(url=INDEX, headers=HEADERS, data=data)
    return response.status_code


if __name__ == '__main__':
    main()
