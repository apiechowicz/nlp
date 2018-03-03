from typing import Tuple

from matplotlib import pyplot
from tqdm import tqdm

from hw1.utils.argument_parser import parse_input_dir_argument
from hw1.utils.file_utils import *
from hw1.utils.regex_utils import find_pattern_in_string, MONEY_PATTERN, convert_money_string_to_int, DETRIMENT_PATTERN


def main() -> None:
    input_dir, judgement_year = parse_input_dir_argument()
    numbers = get_number_data(input_dir, judgement_year)
    save_number_data(numbers, MONEY_NUMBER_DATA_FILENAME)
    exercise1(numbers, judgement_year)
    exercise2(numbers, judgement_year)
    exercise4(input_dir, judgement_year)


def get_number_data(input_dir, judgement_year):
    numbers = load_number_data()
    if len(numbers) == 0:
        numbers = prepare_numbers_data(input_dir, judgement_year)
    return numbers


def prepare_numbers_data(input_dir: str, judgement_year: int) -> List[int]:
    numbers = []
    files_to_be_processed = get_files_to_be_processed(input_dir)
    for filename in tqdm(files_to_be_processed):  # todo format tqdm progressbar
        file = get_absolute_path(input_dir, filename)
        judgements_to_be_processed = extract_judgements_from_given_year_from_file(file, judgement_year)
        for judgement in judgements_to_be_processed:
            content = extract_judgement_content(judgement)
            matches = find_pattern_in_string(MONEY_PATTERN, content)
            for match in matches:
                numbers.append(convert_money_string_to_int(match))
    return numbers


def create_histogram(numbers: List[int], filename: str, year: int):
    output_file = get_absolute_path(OUTPUT_DIRECTORY_PATH, filename)
    pyplot.hist(numbers)
    pyplot.title('Number of occurrences of given money\namount across judgements from year {}'.format(str(year)))
    pyplot.xlabel('Money amounts [pln]')
    pyplot.ylabel('Number of occurrences [-]')
    pyplot.grid(True)
    pyplot.savefig(output_file, dpi=150)
    pyplot.close()


def exercise1(numbers: List[int], judgement_year: int):
    create_histogram(numbers, "exercise-1", judgement_year)


def exercise2(numbers: List[int], judgement_year: int):
    a, b = split_list_by_value(numbers, 1000000)
    create_histogram(a, 'exercise-2-upto-1m', judgement_year)
    create_histogram(b, 'exercise-2-from-1m', judgement_year)


def split_list_by_value(numbers: List[int], value: int) -> Tuple[List[int], List[int]]:
    upto, above = [], []
    for number in numbers:
        if number > value:
            above.append(number)
        else:
            upto.append(number)
    return upto, above


def exercise4(input_dir: str, judgement_year: int):
    occurrences = count_words(input_dir, judgement_year)
    save_number_data([occurrences], 'exercise-4.json')


def count_words(input_dir: str, judgement_year: int) -> int:
    occurrences = 0
    files_to_be_processed = get_files_to_be_processed(input_dir)
    for filename in tqdm(files_to_be_processed):  # todo format tqdm progressbar
        file = get_absolute_path(input_dir, filename)
        judgements_to_be_processed = extract_judgements_from_given_year_from_file(file, judgement_year)
        for judgement in judgements_to_be_processed:
            content = extract_judgement_content(judgement)
            matches = find_pattern_in_string(DETRIMENT_PATTERN, content)
            occurrences += len(matches)
    return occurrences


if __name__ == '__main__':
    main()
