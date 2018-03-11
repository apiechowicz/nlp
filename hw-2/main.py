from calendar import monthrange
from json import loads
from os import getcwd
from typing import List

import requests

from utils.argument_parser import parse_arguments
from utils.file_utils import get_json_as_string, CREATE_INDEX_JSON, SEARCH_JUDGEMENTS_BY_DAY, get_files_to_be_processed, \
    extract_and_upload_data

HOST = r'http://localhost:9200'
INDEX_URL = HOST + r'/nlp-hw2'
INDEX_DATA_URL = INDEX_URL + r'/judgements'
HEADERS = {'content-type': 'application/json'}
COUNT_QUERY_URL = INDEX_DATA_URL + r'/_count'


def main():
    input_dir, judgement_year = parse_arguments()
    create_index_with_analyzer()
    files = get_files_to_be_processed(input_dir)
    for file in files:
        extract_and_upload_data(file, judgement_year, INDEX_DATA_URL, HEADERS)
    data = prepare_histogram_data(judgement_year)


def create_index_with_analyzer() -> str:
    data = get_json_as_string(getcwd(), CREATE_INDEX_JSON)
    response = requests.put(url=INDEX_URL, headers=HEADERS, data=data)
    return response.content


def prepare_histogram_data(judgement_year: int) -> List[int]:
    numbers_of_judgements_per_month = []
    for month in range(1, 12 + 1):
        numbers_of_judgements_per_month.append(count_judgements_for_month(judgement_year, month))
    return numbers_of_judgements_per_month


def count_judgements_for_month(judgement_year: int, month: int) -> int:
    last = monthrange(judgement_year, month)[1]
    first_day = get_day(judgement_year, month, 1)
    last_day = get_day(judgement_year, month, last)
    data = get_json_as_string(getcwd(), SEARCH_JUDGEMENTS_BY_DAY).replace('first_day', first_day) \
        .replace('last_day', last_day)
    response = requests.post(url=COUNT_QUERY_URL, headers=HEADERS, data=data)
    data = response.content.decode('utf-8')
    return int(loads(data)["count"])


def get_day(year: int, month: int, day: int):
    str_values = [get_string_number(x) for x in [year, month, day]]
    return '-'.join(str_values)


def get_string_number(x: int):
    return str(x) if len(str(x)) > 1 else '0' + str(x)


if __name__ == '__main__':
    main()
