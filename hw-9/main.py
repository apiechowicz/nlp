from os.path import getsize, basename
from typing import List

from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import get_files_to_be_processed, extract_judgements_from_file, save_data, \
    PREPROCESSED_DATA_DIRECTORY_PATH, read_data_in_directory
from utils.regex_utils import replace_redundant_characters

BYTES_IN_MEGABYTE = 1024 * 1024


def main():
    input_dir, minimum_data_size = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    files = select_random_files(files, minimum_data_size)
    judgements = preprocess_judgements(files)
    judgements = read_data_in_directory(PREPROCESSED_DATA_DIRECTORY_PATH)


def preprocess_judgements(files: List[str]) -> List[str]:
    all_judgements = []
    for file in tqdm(files, unit='files'):
        judgements = extract_judgements_from_file(file)
        judgements = [replace_redundant_characters(judgement["textContent"]) for judgement in judgements]
        all_judgements.extend(judgements)
        save_data(PREPROCESSED_DATA_DIRECTORY_PATH, judgements, basename(file).replace('.json', '.txt'))
    return all_judgements


def select_random_files(files: List[str], minimum_data_size: float) -> List[str]:
    total_size = get_total_size_in_megabytes(files)
    division_point = get_division_point(total_size, minimum_data_size)
    return files[:int(len(files) / division_point)]


def get_total_size_in_megabytes(files: List[str]) -> float:
    return sum([getsize(file) for file in files]) / BYTES_IN_MEGABYTE


def get_division_point(total_size: float, minimum_data_size: float) -> int:
    divider = 1
    while total_size / (divider + 1) > minimum_data_size:
        divider += 1
    return divider + 1 if total_size / divider + 1 >= 0.9 * minimum_data_size else divider


if __name__ == '__main__':
    main()
