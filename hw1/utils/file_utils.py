from json import loads
from os import listdir
from os.path import join, basename
from typing import List, Dict

from hw1.utils.regex_utils import is_valid_input_file, judgement_year_matches


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


def extract_judgement_content(judgement: Dict[str, str]):
    return judgement["textContent"]
