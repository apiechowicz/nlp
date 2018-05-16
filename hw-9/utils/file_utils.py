from json import loads
from os import listdir, getcwd, makedirs
from os.path import join, isdir
from typing import List, Dict

from utils.regex_utils import is_valid_input_file

OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)
PREPROCESSED_DATA_DIRECTORY_PATH = join(OUTPUT_DIRECTORY_PATH, r'preprocessed-data')
PHRASES_DATA_DIRECTORY_PATH = join(OUTPUT_DIRECTORY_PATH, r'phrases-data')
EXTENSION = r'.txt'


def get_files_to_be_processed(input_dir: str) -> List[str]:
    files_to_be_processed = []
    for filename in listdir(input_dir):
        if is_valid_input_file(filename):
            files_to_be_processed.append(join(input_dir, filename))
    return files_to_be_processed


def extract_judgements_from_file(file: str) -> List[Dict[str, str]]:
    with open(file) as f:
        content = f.read()
        json_data = loads(content)
        judgements = json_data["items"]
        return judgements


def save_data(judgements: List[str], file_name: str) -> None:
    create_dir(OUTPUT_DIRECTORY_PATH)
    with open(join(OUTPUT_DIRECTORY_PATH, file_name), 'w') as file:
        for judgement in judgements:
            file.write(judgement + '\n')


def create_dir(path: str) -> None:
    if not isdir(path):
        makedirs(path)


def read_data(file_name: str) -> List[str]:
    judgements = []
    with open(join(OUTPUT_DIRECTORY_PATH, file_name), 'r') as file:
        for line in file:
            judgements.append(line.rstrip())
    return judgements
