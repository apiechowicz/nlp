from datetime import datetime
from json import loads
from os import listdir, getcwd, makedirs
from re import fullmatch
from typing import List, Dict

import requests
from os.path import join, isdir, basename

from utils.regex_utils import replace_all_redundant_characters

INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = r'%Y-%m-%d'
OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)
ENCODING = r'utf-8'
TAGGED_JUDGEMENTS_DIRECTORY_NAME = r'tagged-judgements'


def get_files_to_be_processed(input_dir: str) -> List[str]:
    files_to_be_processed = []
    for filename in listdir(input_dir):
        if is_valid_input_file(filename):
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
    create_output_dir(join(OUTPUT_DIRECTORY_PATH, TAGGED_JUDGEMENTS_DIRECTORY_NAME))
    filename = '{}-{}.txt'.format(judgement_filename.replace('.json', ''), judgement_number)
    with open(join(OUTPUT_DIRECTORY_PATH, TAGGED_JUDGEMENTS_DIRECTORY_NAME, filename), 'w+') as file:
        file.write(data)


def create_output_dir(path: str):
    if not isdir(path):
        makedirs(path)
