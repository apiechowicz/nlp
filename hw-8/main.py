from json import loads
from time import sleep
from typing import List, Dict

from requests import post, get
from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import extract_judgements_from_given_year_from_file, get_json_as_string, read_data, \
    get_files_to_be_processed, save_data
from utils.regex_utils import replace_redundant_characters

ENCODING = r'utf-8'
API_PATH = r'http://ws.clarin-pl.eu/nlprest2/base'
HEADERS = {'content-type': 'application/json', 'charset': '{}'.format(ENCODING)}
START_TASK_PATH = API_PATH + r'/startTask'
GET_STATUS_PATH = API_PATH + r'/getStatus/{}'
GET_FILE_PATH = API_PATH + r'/download/{}'


def main():
    input_dir, judgement_year, n = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    judgements = extract_judgements(files, judgement_year)
    judgements = sort_and_take_n_judgements(judgements, n)
    save_data(judgements, 'data.txt')
    judgements = read_data('data.txt')
    task_ids = create_ner_tasks(judgements)
    save_data(task_ids, 'tasks.txt')
    task_ids = read_data('tasks.txt')
    task_map = create_task_map(task_ids)
    task_map = wait_for_tasks_to_complete(task_map)


def extract_judgements(files, judgement_year):
    judgements = []
    for file in tqdm(files, unit='files'):
        judgements.extend(extract_judgements_from_given_year_from_file(file, judgement_year))
    return judgements


def sort_and_take_n_judgements(judgements, n):
    sorted_judgements = [replace_redundant_characters(judgement['textContent']) for judgement
                         in sorted(judgements, key=lambda judgement: judgement['judgmentDate'])]
    return sorted_judgements[:n]


def create_ner_tasks(judgements: List[str]) -> List[str]:
    return [create_ner_task(judgement) for judgement in judgements]


def create_ner_task(judgement: str) -> str:
    data = get_json_as_string('start-task.json').replace('query_data', judgement).encode(ENCODING)
    response = post(url=START_TASK_PATH, headers=HEADERS, data=data)
    return response.content.decode(ENCODING)


def create_task_map(task_ids: List[str]) -> Dict[str, Dict[str, str]]:
    tasks_with_status = {task_id: get_task_status(task_id) for task_id in task_ids}
    return tasks_with_status


def get_task_status(task_id: str) -> Dict[str, str]:
    response = get(url=GET_STATUS_PATH.format(task_id))
    return loads(response.content.decode(ENCODING))


def wait_for_tasks_to_complete(task_map: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    not_completed = [task_id for task_id in task_map.keys() if not is_completed(task_map, task_id)]
    while len(not_completed) > 0:
        now_completed = []
        for task_id in not_completed:
            task_map[task_id] = get_task_status(task_id)
            if is_completed(task_map, task_id):
                now_completed.append(task_id)
            sleep(3)
        for completed in now_completed:
            not_completed.remove(completed)
    return task_map


def is_completed(task_map: Dict[str, Dict[str, str]], task_id: str) -> bool:
    return task_map[task_id]['status'] == 'DONE'


if __name__ == '__main__':
    main()
