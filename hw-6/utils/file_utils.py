from json import loads
from os import listdir, getcwd, makedirs
from os.path import join, isdir
from typing import List, Dict

from utils.regex_utils import is_valid_input_file, judgement_year_matches, get_judgement_date, ALL_LABELS

OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)
TOP_WORDS_FILE = join(getcwd(), '../hw-3/out/exercise-2.txt')
DATA_FILE_EXTENSION = r'.txt'


def get_files_to_be_processed(input_dir: str) -> List[str]:
    files_to_be_processed = []
    for filename in listdir(input_dir):
        if is_valid_input_file(filename):
            files_to_be_processed.append(join(input_dir, filename))
    return files_to_be_processed


def get_absolute_path(filename: str, directory: str):
    return join(directory, filename)


def extract_judgements_from_given_year_from_file(file: str, year: int) -> List[Dict[str, str]]:
    with open(file) as f:
        content = f.read()
        json_data = loads(content)
        judgements = json_data["items"]
        judgements = [judgement for judgement in judgements
                      if judgement_year_matches(get_judgement_date(judgement), year)]
        return judgements


def read_top_n_words(n_words: int) -> List[str]:
    top_words = []
    with open(TOP_WORDS_FILE, 'r') as file:
        all_words = eval(file.read())
        i = 0
        for word, occurrences in all_words:
            if len(word) > 1:
                top_words.append(word)
                i += 1
            if i == n_words:
                break
    return top_words


def save_data(judgements_by_type: Dict[str, List[str]]) -> None:
    create_output_dir(OUTPUT_DIRECTORY_PATH)
    for label in judgements_by_type.keys():
        with open(join(OUTPUT_DIRECTORY_PATH, label + DATA_FILE_EXTENSION), 'w') as file:
            for substantiation in judgements_by_type[label]:
                file.write(substantiation + '\n')


def create_output_dir(path: str) -> None:
    if not isdir(path):
        makedirs(path)


def read_data() -> Dict[str, List[str]]:
    judgements_by_type = dict()
    for label in ALL_LABELS:
        judgements_by_type[label] = list()
        with open(join(OUTPUT_DIRECTORY_PATH, label + DATA_FILE_EXTENSION), 'r') as file:
            for line in file:
                judgements_by_type[label].append(line.rstrip())
    return judgements_by_type
