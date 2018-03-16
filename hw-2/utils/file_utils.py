from datetime import datetime
from json import loads, dumps
from os import listdir, getcwd, makedirs
from os.path import join, isdir
from re import fullmatch
from typing import List, Dict

import requests

JSONS_DIRECTORY = r'jsons'
CREATE_INDEX_JSON = r'create-index-with-analyzer.json'
INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = r'%Y-%m-%d'
SEARCH_DETRIMENT_WORD = r'search-detriment-word.json'
SEARCH_JUDGEMENTS_BY_DAY = r'search-judgements-by-date.json'
SEARCH_PHRASE = r'search-phrase.json'
SEARCH_JUDGES = r'search-top-judges.json'
OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)


def get_json_as_string(working_dir: str, file_name: str) -> str:
    return __read_json_file_to_string(join(working_dir, JSONS_DIRECTORY, file_name))


def __read_json_file_to_string(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read().replace('\n', '')


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
        content = file.read()
        content_as_json = loads(content)
        judgements = content_as_json["items"]
        for judgement in judgements:
            if __judgement_year_matches(judgement["judgmentDate"], year):
                data = __get_required_data(judgement)
                requests.post(url=url, headers=headers, data=data)


def __judgement_year_matches(date: str, year: int) -> bool:
    return datetime.strptime(date, JUDGEMENT_DATE_FORMAT).year == year


def __get_required_data(judgement: Dict):
    data = {"textContent": judgement["textContent"], "judgmentDate": judgement["judgmentDate"],
            "caseNumber": judgement["courtCases"][0]["caseNumber"], "judges": __extract_only_judges_names(judgement)}
    return dumps(data) + '\n'


def __extract_only_judges_names(judgement: Dict) -> List[Dict[str, str]]:
    result = []
    for judge in judgement["judges"]:
        result.append({"name": judge["name"]})
    return result


def create_output_dir():
    if not isdir(OUTPUT_DIRECTORY_PATH):
        makedirs(OUTPUT_DIRECTORY_PATH)


def save_data(data: str, filename: str):
    create_output_dir()
    with open(join(OUTPUT_DIRECTORY_PATH, filename), 'w+') as file:
        file.write(data)
