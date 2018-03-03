from typing import List

from matplotlib import pyplot

from hw1.utils.argument_parser import parse_input_dir_argument
from hw1.utils.file_utils import get_files_to_be_processed, get_absolute_path, \
    extract_judgements_from_given_year_from_file, \
    extract_judgement_content
from hw1.utils.regex_utils import find_money_in_string, convert_money_string_to_int


def main() -> None:
    input_dir, judgement_year = parse_input_dir_argument()
    numbers = prepare_numbers_data(input_dir, judgement_year)
    pyplot.hist(numbers)
    pyplot.show()


def prepare_numbers_data(input_dir: str, judgement_year: int) -> List[int]:
    files_to_be_processed = get_files_to_be_processed(input_dir)
    numbers = []
    for filename in files_to_be_processed:  # todo add tqdm progressbar
        file = get_absolute_path(input_dir, filename)
        judgements_to_be_processed = extract_judgements_from_given_year_from_file(file, judgement_year)
        for judgement in judgements_to_be_processed:
            content = extract_judgement_content(judgement)
            match = find_money_in_string(content)
            for number in match:
                numbers.append(convert_money_string_to_int(number))
    return numbers


if __name__ == '__main__':
    main()
