from os import listdir
from os.path import join
from re import fullmatch
from typing import List

INPUT_FILE_NAME_PATTERN = 'judgments-\d+\.json'


def get_files_to_be_processed(input_dir: str) -> List[str]:
    files_to_be_processed = []
    for filename in listdir(input_dir):
        if fullmatch(INPUT_FILE_NAME_PATTERN, filename):
            files_to_be_processed.append(filename)
    return files_to_be_processed


def get_absolute_path(input_dir: str, filename: str) -> str:
    return join(input_dir, filename)
