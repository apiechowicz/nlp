from typing import Tuple, List, Dict

from matplotlib import pyplot
from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import get_files_to_be_processed, get_absolute_path, \
    extract_judgements_from_given_year_from_file, extract_from_judgement, OUTPUT_DIRECTORY_PATH, save_data, \
    create_output_dir
from utils.regex_utils import find_pattern_in_string, MONEY_PATTERN, convert_money_string_to_int, \
    DETRIMENT_PATTERN, LAW_NAME, find_pattern_once_in_string, ARTICLE_PATTERN


def main() -> None:
    input_dir, judgement_year, dividing_point = parse_arguments()
    files_to_be_processed = get_files_to_be_processed(input_dir)
    numbers, references_number, detriment_words_number = process_files(files_to_be_processed, input_dir, judgement_year)
    exercise1(numbers, judgement_year)
    exercise2(numbers, dividing_point, judgement_year)
    exercise3(references_number, judgement_year)
    exercise4(detriment_words_number, judgement_year)


def process_files(files_to_be_processed: List[str], input_dir: str, judgement_year: int) -> Tuple[List[int], int, int]:
    numbers, references_number, judgements_with_detriment_word = [], 0, 0
    for filename in tqdm(files_to_be_processed, mininterval=10, unit='files'):
        file = get_absolute_path(input_dir, filename)
        judgements_to_be_processed = extract_judgements_from_given_year_from_file(file, judgement_year)
        for judgement in judgements_to_be_processed:
            content = extract_from_judgement(judgement, 'textContent')
            find_money_in_content(content, numbers)  # collect data for exercise 1 and 2
            regulations = extract_from_judgement(judgement, 'referencedRegulations')  # collect data for exercise 3
            for regulation in regulations:
                if references_given_law_article(regulation, LAW_NAME, ARTICLE_PATTERN):
                    references_number += 1
                    break
            match = find_pattern_once_in_string(DETRIMENT_PATTERN, content)  # collect data for exercise 4
            if match is not None:
                judgements_with_detriment_word += 1
    return numbers, references_number, judgements_with_detriment_word


def find_money_in_content(content: str, numbers: List[int]):
    matches = find_pattern_in_string(MONEY_PATTERN, content)
    for match in matches:
        numbers.append(convert_money_string_to_int(match))


def references_given_law_article(regulation: Dict[str, str], law_name: str, article_pattern: str) -> bool:
    return regulation['journalTitle'] == law_name \
           and find_pattern_once_in_string(article_pattern, regulation['text']) is not None


def exercise1(numbers: List[int], judgement_year: int):
    create_histogram(numbers, "exercise-1", judgement_year)
    save_data('There have been {0} money amounts in judgements from year {1}.'.format(len(numbers), judgement_year),
              'exercise-1.txt')


def create_histogram(numbers: List[int], filename: str, year: int):
    output_file = get_absolute_path(OUTPUT_DIRECTORY_PATH, filename)
    create_output_dir()
    pyplot.hist(numbers)
    pyplot.title('Number of occurrences of given money\namount across judgements from year {}'.format(str(year)))
    pyplot.xlabel('Money amounts [pln]')
    pyplot.ylabel('Number of occurrences [-]')
    pyplot.grid(True)
    pyplot.savefig(output_file, dpi=150)
    pyplot.close()


def exercise2(numbers: List[int], dividing_point: int, judgement_year: int):
    a, b = split_list_by_value(numbers, dividing_point)
    create_histogram(a, 'exercise-2-upto-{}'.format(dividing_point), judgement_year)
    create_histogram(b, 'exercise-2-above-{}'.format(dividing_point), judgement_year)
    save_data('There have been {0} numbers up to {1} and {2} above that amount in year {3}.'
              .format(len(a), dividing_point, len(b), judgement_year),
              'exercise-2.txt')


def split_list_by_value(numbers: List[int], value: int) -> Tuple[List[int], List[int]]:
    upto, above = [], []
    for number in numbers:
        if number > value:
            above.append(number)
        else:
            upto.append(number)
    return upto, above


def exercise3(occurrences: int, judgement_year: int):
    save_data('There have been {0} judgements referencing given article in {1}.'.format(occurrences, judgement_year),
              'exercise-3.txt')


def exercise4(occurrences: int, judgement_year: int):
    save_data('There have been {0} judgements containing given word in {1}.'.format(occurrences, judgement_year),
              'exercise-4.txt')


if __name__ == '__main__':
    main()
