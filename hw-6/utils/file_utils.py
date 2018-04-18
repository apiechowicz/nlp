from json import loads
from os import listdir, getcwd
from os.path import join
from typing import List, Dict

from utils.regex_utils import is_valid_input_file, judgement_year_matches, get_judgement_date

OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)
TOP_WORDS_FILE = join(getcwd(), '../hw-3/out/exercise-2.txt')


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
