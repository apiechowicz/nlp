from _elementtree import Element
from json import loads
from time import sleep, time
from typing import List, Dict
from xml.etree import ElementTree as etree

from requests import post, get
from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import extract_judgements_from_given_year_from_file, get_json_as_string, \
    read_task_results
from utils.regex_utils import replace_redundant_characters

ENCODING = r'utf-8'
API_PATH = r'http://ws.clarin-pl.eu/nlprest2/base'
HEADERS = {'content-type': 'application/json', 'charset': '{}'.format(ENCODING)}
START_TASK_PATH = API_PATH + r'/startTask'
GET_STATUS_PATH = API_PATH + r'/getStatus/{}'
GET_FILE_PATH = API_PATH + r'/download'


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
    task_map = {task_id: get_result(task_map[task_id]) for task_id in task_map.keys()}
    save_task_results(task_map)
    task_results = read_task_results()
    category_map = create_category_map(task_results)
    super_category_map = create_super_category_map(category_map)


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


def create_task_map(task_ids: List[str]) -> Dict:
    tasks_with_status = {task_id: get_task_status(task_id) for task_id in task_ids}
    return tasks_with_status


def get_task_status(task_id: str) -> List[Dict[str, str]]:
    response = get(url=GET_STATUS_PATH.format(task_id))
    return loads(response.content.decode(ENCODING))


def wait_for_tasks_to_complete(task_map: Dict) -> Dict:
    print('Waiting for tasks to complete...')
    not_completed = [task_id for task_id in task_map.keys() if not is_completed(task_map, task_id)]
    start = time()
    while len(not_completed) > 0:
        print('Tasks left: ' + str(len(not_completed)))
        now_completed = []
        for task_id in not_completed:
            task_map[task_id] = get_task_status(task_id)
            if is_completed(task_map, task_id):
                now_completed.append(task_id)
            sleep(1)
        for completed in now_completed:
            not_completed.remove(completed)
    print('Waiting took: {}s'.format(round(time() - start, 2)))
    return task_map


def is_completed(task_map: Dict, task_id: str) -> bool:
    return task_map[task_id]['status'] == 'DONE'


def get_result(status: Dict) -> str:
    file_path = status['value'][0]['fileID']
    response = get(url=GET_FILE_PATH + file_path)
    return response.content.decode(ENCODING)


def create_category_map(task_results: List[str]) -> Dict[str, Dict[str, int]]:
    category_map = {}
    for xml in task_results:
        chunk_list = etree.fromstring(xml)
        for chunk in chunk_list:
            for sentence in chunk:
                for token in sentence:
                    if token.tag == 'tok':
                        parse_token(token, category_map)
    return category_map


def parse_token(token: Element, category_map: Dict[str, Dict[str, int]]) -> None:
    word = ''
    categories = []
    for child in token:
        if child.tag == 'orth':
            # todo should I use tok.orth or rather tok.lex.base?
            word = child.text
        elif child.tag == 'ann':
            # todo what does the number inside the tag mean?
            categories.append(child.get('chan'))
    if word != '' and len(categories) > 0:
        update_category_map(category_map, categories, word)


def update_category_map(category_map: Dict[str, Dict[str, int]], categories: List[str], word: str) -> None:
    for category in categories:
        if category not in category_map:
            category_map[category] = {}
        if word not in category_map[category]:
            category_map[category][word] = 1
        else:
            category_map[category][word] += 1


def create_super_category_map(category_map: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
    super_category_map = {}
    for category in category_map.keys():
        super_category = '_'.join(category.split('_')[:2])
        if super_category not in super_category_map:
            super_category_map[super_category] = {}
        for word in category_map[category].keys():
            if word not in super_category_map[super_category]:
                super_category_map[super_category][word] = category_map[category][word]
            else:
                super_category_map[super_category][word] += category_map[category][word]
    return super_category_map


if __name__ == '__main__':
    main()
