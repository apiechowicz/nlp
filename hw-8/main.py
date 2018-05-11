from typing import List

from requests import post
from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import get_files_to_be_processed, extract_judgements_from_given_year_from_file, save_data, \
    read_data, get_json_as_string
from utils.regex_utils import replace_redundant_characters

ENCODING = r'utf-8'
HOST = r'http://ws.clarin-pl.eu'
HEADERS = {'content-type': 'application/json', 'charset': '{}'.format(ENCODING)}
START_TASK_PATH = HOST + r'/nlprest2/base/startTask'
GET_STATUS_PATH = HOST + r'/nlprest2/base/getStatus/{}'


def main():
    input_dir, judgement_year, n = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    judgements = extract_judgements(files, judgement_year)
    judgements = sort_and_take_n_judgements(judgements, n)
    save_data(judgements, 'data.txt')
    judgements = read_data('data.txt')
    jobs_ids = create_ner_tasks(judgements)
    save_data(jobs_ids, 'jobs.txt')
    jobs_ids = read_data('jobs.txt')
    # todo read data from processed jobs


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


if __name__ == '__main__':
    main()
