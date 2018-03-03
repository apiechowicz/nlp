from matplotlib import pyplot
from tqdm import tqdm

from hw1.utils.argument_parser import parse_input_dir_argument
from hw1.utils.file_utils import *
from hw1.utils.regex_utils import find_money_in_string, convert_money_string_to_int


def main() -> None:
    input_dir, judgement_year = parse_input_dir_argument()
    numbers = get_number_data(input_dir, judgement_year)
    save_number_data(numbers)
    create_histogram(numbers, "ex1")


def get_number_data(input_dir, judgement_year):
    numbers = load_number_data()
    if len(numbers) == 0:
        numbers = prepare_numbers_data(input_dir, judgement_year)
    return numbers


def prepare_numbers_data(input_dir: str, judgement_year: int) -> List[int]:
    files_to_be_processed = get_files_to_be_processed(input_dir)
    numbers = []
    for filename in tqdm(files_to_be_processed):  # todo format tqdm progressbar
        file = get_absolute_path(input_dir, filename)
        judgements_to_be_processed = extract_judgements_from_given_year_from_file(file, judgement_year)
        for judgement in judgements_to_be_processed:
            content = extract_judgement_content(judgement)
            match = find_money_in_string(content)
            for number in match:
                numbers.append(convert_money_string_to_int(number))
    return numbers


def create_histogram(numbers: List[int], filename: str):
    pyplot.hist(numbers)
    output_file = get_absolute_path(OUTPUT_DIRECTORY_PATH, filename)
    pyplot.savefig(output_file)


if __name__ == '__main__':
    main()
