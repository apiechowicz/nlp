from json import loads
from os import listdir, getcwd, makedirs
from os.path import join, isdir
from typing import List, Iterable

from utils.regex_utils import *

OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)


def get_files_to_be_processed(input_dir: str) -> List[str]:
    files_to_be_processed = []
    for filename in listdir(input_dir):
        if is_valid_input_file(filename):
            files_to_be_processed.append(join(input_dir, filename))
    return files_to_be_processed


def extract_judgements_from_given_year_from_file(file: str, year: int) -> List[Dict[str, str]]:
    with open(file) as f:
        content = f.read()
        json_data = loads(content)
        judgements = json_data["items"]
        judgements = [judgement for judgement in judgements
                      if judgement_year_matches(get_judgement_date(judgement), year)]
        return judgements


def save_data(data: Iterable, filename: str):
    create_output_dir()
    with open(join(OUTPUT_DIRECTORY_PATH, filename), 'w+') as file:
        for element in data:
            file.write(str(element) + '\n')


def create_output_dir():
    if not isdir(OUTPUT_DIRECTORY_PATH):
        makedirs(OUTPUT_DIRECTORY_PATH)


def read_data(filename: str) -> List:
    with open(join(OUTPUT_DIRECTORY_PATH, filename), 'r') as file:
        data = []
        for line in file:
            data.append(eval(line))
        return data
