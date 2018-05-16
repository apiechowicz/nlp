from json import loads
from os import listdir, getcwd, makedirs
from os.path import join, isdir
from typing import List, Dict

from utils.regex_utils import is_valid_input_file, judgement_year_matches

OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)
JSONS_DIRECTORY = r'jsons'
TASKS_DIRECTORY_PATH = join(OUTPUT_DIRECTORY_PATH, r'task-results')
TASK_RESULTS_EXTENSION = r'.xml'


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
        judgements = [judgement for judgement in judgements if judgement_year_matches(judgement['judgmentDate'], year)]
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


def get_json_as_string(file_name: str) -> str:
    return __read_json_file_to_string(join(getcwd(), JSONS_DIRECTORY, file_name))


def __read_json_file_to_string(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read().replace('\n', '')


def save_task_results(task_map: Dict[str, str]) -> None:
    create_dir(TASKS_DIRECTORY_PATH)
    for task_id in task_map.keys():
        with open(__get_task_result_filename(task_id), 'w') as file:
            file.write(task_map[task_id])


def __get_task_result_filename(task_id: str) -> str:
    return join(TASKS_DIRECTORY_PATH, task_id + TASK_RESULTS_EXTENSION)


def read_task_results() -> List[str]:
    create_dir(TASKS_DIRECTORY_PATH)
    results = []
    for file_name in listdir(TASKS_DIRECTORY_PATH):
        with open(join(TASKS_DIRECTORY_PATH, file_name)) as file:
            results.append(file.read())
    return results
