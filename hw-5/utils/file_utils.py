from datetime import datetime
from json import loads
from os import listdir, getcwd
from re import fullmatch
from typing import List, Dict

import requests
from os.path import join

INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = r'%Y-%m-%d'
OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)


def get_files_to_be_processed(input_dir: str) -> List[str]:
    files_to_be_processed = []
    for filename in listdir(input_dir):
        if is_valid_input_file(filename):
            files_to_be_processed.append(join(input_dir, filename))
    return files_to_be_processed


def is_valid_input_file(filename: str) -> bool:
    return fullmatch(INPUT_FILE_NAME_PATTERN, filename) is not None


def extract_and_upload_data(file_path: str, year: int, url: str, headers: Dict[str, str]):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        content_as_json = loads(content)
        judgements = content_as_json["items"]
        for judgement in judgements:
            if __judgement_year_matches(judgement["judgmentDate"], year):
                requests.post(url=url, headers=headers, data=judgement["textContent"].encode('utf-8'))


def __judgement_year_matches(date: str, year: int) -> bool:
    return datetime.strptime(date, JUDGEMENT_DATE_FORMAT).year == year
