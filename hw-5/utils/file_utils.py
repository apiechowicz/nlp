from datetime import datetime
from json import loads
from os import listdir, getcwd, makedirs
from re import fullmatch
from typing import List, Dict, Callable, Iterable

import requests
from os.path import join, isdir, basename

from utils.regex_utils import replace_all_redundant_characters

INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = r'%Y-%m-%d'
OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)
ENCODING = r'utf-8'
TAGGED_JUDGEMENTS_DIRECTORY_NAME = r'tagged-judgements'
TAGGED_JUDGEMENTS_DIRECTORY = join(OUTPUT_DIRECTORY_PATH, TAGGED_JUDGEMENTS_DIRECTORY_NAME)


def get_files_to_be_processed(input_dir: str, filename_validating_function: Callable[[str], bool]) -> List[str]:
    files_to_be_processed = []
    for filename in listdir(input_dir):
        if filename_validating_function(filename):
            files_to_be_processed.append(join(input_dir, filename))
    return files_to_be_processed


def is_valid_input_file(filename: str) -> bool:
    return fullmatch(INPUT_FILE_NAME_PATTERN, filename) is not None


def extract_and_upload_data(file_path: str, year: int, url: str, headers: Dict[str, str]):
    with open(file_path, 'r') as file:
        judgements = __get_judgements(file)
        judgement_number = 0
        for judgement in judgements:
            if __judgement_year_matches(judgement["judgmentDate"], year):
                judgement_number += 1
                data = replace_all_redundant_characters(judgement["textContent"])
                response = requests.post(url=url, headers=headers, data=data.encode(ENCODING))
                response_data = response.content.decode(ENCODING)
                save_tagged_judgement(response_data, basename(file_path), judgement_number)


def __get_judgements(file) -> List[Dict[str, str]]:
    content = file.read()
    content_as_json = loads(content)
    judgements = content_as_json["items"]
    return judgements


def __judgement_year_matches(date: str, year: int) -> bool:
    return datetime.strptime(date, JUDGEMENT_DATE_FORMAT).year == year


def save_tagged_judgement(data: str, judgement_filename: str, judgement_number: int):
    create_output_dir(TAGGED_JUDGEMENTS_DIRECTORY)
    filename = '{}-{}.txt'.format(judgement_filename.replace('.json', ''), judgement_number)
    with open(join(TAGGED_JUDGEMENTS_DIRECTORY, filename), 'w+') as file:
        file.write(data)


def create_output_dir(path: str):
    if not isdir(path):
        makedirs(path)


def get_words_from_tagged_judgement(file_path: str) -> List[str]:
    words = []
    with open(file_path) as file:
        for line in file:
            if ':' in line:
                word = ':'.join(line.strip().replace('\t', ':').split(':')[:2])
                words.append(word)
    return words


def save_data(data: Iterable, filename: str):
    create_output_dir(OUTPUT_DIRECTORY_PATH)
    with open(join(OUTPUT_DIRECTORY_PATH, filename), 'w+') as file:
        for element in data:
            file.write(str(element) + '\n')


def read_data(filename: str) -> List:
    with open(join(OUTPUT_DIRECTORY_PATH, filename), 'r') as file:
        data = []
        for line in file:
            data.append(eval(line))
        return data
