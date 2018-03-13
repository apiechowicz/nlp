from calendar import monthrange
from json import loads
from os import getcwd
from os.path import join
from typing import List

import requests
from matplotlib import pyplot
from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import get_json_as_string, CREATE_INDEX_JSON, SEARCH_JUDGEMENTS_BY_DAY, SEARCH_DETRIMENT_WORD, \
    save_data, OUTPUT_DIRECTORY_PATH, create_output_dir, get_files_to_be_processed, extract_and_upload_data, \
    SEARCH_PHRASE, SEARCH_JUDGES

HOST = r'http://localhost:9200'
INDEX_URL = HOST + r'/nlp-hw2'
INDEX_DATA_URL = INDEX_URL + r'/judgements'
COUNT_QUERY_URL = INDEX_DATA_URL + r'/_count'
SEARCH_QUERY_URL = INDEX_DATA_URL + r'/_search'
HEADERS = {'content-type': 'application/json'}
DETRIMENT_WORD = r'szkoda'
PHRASE = r'trwały uszczerbek na zdrowiu'
NUMBER_OF_JUDGES = 3


def main():
    input_dir, judgement_year = parse_arguments()
    create_index_with_analyzer()
    files = get_files_to_be_processed(input_dir)
    for file in tqdm(files, mininterval=15, unit='files'):
        extract_and_upload_data(file, judgement_year, INDEX_DATA_URL, HEADERS)
    save_data('Word {} occurred {} times in judgements from year {}.'.format(DETRIMENT_WORD, count_detriment_words(),
                                                                             judgement_year), 'exercise-6.txt')
    save_data(
        'Given phrase has occurred {} times in judgements from year {}.'.format(find_phrase(PHRASE, 0), judgement_year),
        'exercise-7.txt')
    save_data(
        'Given phrase has occurred {} times in judgements from year {}.'.format(find_phrase(PHRASE, 2), judgement_year),
        'exercise-8.txt')
    save_data(search_top_judges(NUMBER_OF_JUDGES, judgement_year), 'exercise-9.txt')
    create_bar_chart(prepare_bar_chart_data(judgement_year), 'exercise-10.png', judgement_year)


def create_index_with_analyzer() -> str:
    data = get_json_as_string(getcwd(), CREATE_INDEX_JSON)
    response = requests.put(url=INDEX_URL, headers=HEADERS, data=data)
    return response.content


def __get_count_from_response(response) -> int:
    response_data = response.content.decode('utf-8')
    return int(loads(response_data)["count"])


def prepare_bar_chart_data(judgement_year: int) -> List[int]:
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
    return __get_count_from_response(response)


def get_day(year: int, month: int, day: int):
    str_values = [get_string_number(x) for x in [year, month, day]]
    return '-'.join(str_values)


def get_string_number(x: int):
    return str(x) if len(str(x)) > 1 else '0' + str(x)


def count_detriment_words():
    data = get_json_as_string(getcwd(), SEARCH_DETRIMENT_WORD).replace('detriment_word', DETRIMENT_WORD)
    response = requests.post(url=COUNT_QUERY_URL, headers=HEADERS, data=data)
    return __get_count_from_response(response)


def find_phrase(phrase: str, slop: int) -> int:
    data = get_json_as_string(getcwd(), SEARCH_PHRASE).replace('query_phrase', phrase) \
        .replace('slop_number', str(slop)).encode('utf-8')
    response = requests.post(url=COUNT_QUERY_URL, headers=HEADERS, data=data)
    return __get_count_from_response(response)


def search_top_judges(number_of_judges: int, judgement_year: int) -> str:
    data = get_json_as_string(getcwd(), SEARCH_JUDGES).replace('number_of_judges', str(number_of_judges))
    response = requests.post(url=SEARCH_QUERY_URL, headers=HEADERS, data=data)
    response_data = loads(response.content.decode('utf-8'))
    top_judges_list = response_data["aggregations"]["judges"]["top_judges_names"]["buckets"]
    result = 'Top {} judges by number of judgements in year {}:\n'.format(number_of_judges, judgement_year)
    for pair in top_judges_list:
        result += '{} - {}\n'.format(pair['key'], pair['doc_count'])
    return result


def create_bar_chart(numbers: List[int], filename: str, year: int):
    output_file = join(OUTPUT_DIRECTORY_PATH, filename)
    create_output_dir()
    pyplot.bar(range(1, 12 + 1), numbers)
    pyplot.xticks(range(1, 12 + 1))
    pyplot.title('Number of judgements per month in year {}'.format(str(year)))
    pyplot.xlabel('Month [-]')
    pyplot.ylabel('Number of judgements [-]')
    pyplot.grid(True)
    pyplot.savefig(output_file, dpi=150)
    pyplot.close()


if __name__ == '__main__':
    main()
