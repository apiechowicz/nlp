from json import loads
from os import getcwd
from os import listdir, makedirs
from os.path import join, basename, isdir
from typing import List, Dict

from hw1.utils.regex_utils import is_valid_input_file, judgement_year_matches

OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)
MONEY_NUMBER_DATA_FILENAME = r'number-data.json'


def get_files_to_be_processed(input_dir: str) -> List[str]:
    files_to_be_processed = []
    for filename in listdir(input_dir):
        if is_valid_input_file(filename):
            files_to_be_processed.append(filename)
    return files_to_be_processed


def get_absolute_path(input_dir: str, filename: str) -> str:
    return join(input_dir, filename)


def get_filename(absolute_path: str) -> str:
    return basename(absolute_path)


def extract_judgements_from_given_year_from_file(file: str, year: int) -> List[Dict[str, str]]:
    with open(file) as f:
        content = f.read()
        json_data = loads(content)
        judgements = json_data["items"]
        judgements = [judgement for judgement in judgements
                      if judgement_year_matches(__get_judgement_date(judgement), year)]
        return judgements


def __get_judgement_date(judgement: Dict[str, str]) -> str:
    return judgement["judgmentDate"]


def extract_from_judgement(judgement: Dict[str, str], field_name: str):
    return judgement[field_name]


def create_output_dir():
    if not isdir(OUTPUT_DIRECTORY_PATH):
        makedirs(OUTPUT_DIRECTORY_PATH)


def save_data(data: str, filename: str):
    create_output_dir()
    with open(join(OUTPUT_DIRECTORY_PATH, filename), 'w+') as file:
        file.write(data)
