from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import get_files_to_be_processed, extract_judgements_from_given_year_from_file, \
    get_absolute_path, read_top_n_words, save_data
from utils.regex_utils import *


def main():
    input_dir, judgement_year, replace_n, test_data_percentage = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    judgements_by_type = get_judgements_by_type_dict()
    for file in tqdm(files, unit='files'):
        extract_judgements_from_file(file, input_dir, judgement_year, judgements_by_type, replace_n)
    save_data(judgements_by_type)
    # judgements_by_type = read_data()


def get_judgements_by_type_dict() -> Dict[str, List[str]]:
    judgements_by_type = dict()
    for label in ALL_LABELS:
        judgements_by_type[label] = []
    return judgements_by_type


def extract_judgements_from_file(file: str, input_dir: str, judgement_year: int,
                                 judgements_by_type: Dict[str, List[str]], replace_n: int) -> None:
    judgements = extract_judgements_from_given_year_from_file(get_absolute_path(file, input_dir), judgement_year)
    for judgement in judgements:
        if is_common_or_supreme_court_judgement(judgement):
            case_label = get_case_label(judgement)
            if case_label is not None:
                content = extract_from_judgement(judgement, 'textContent')
                content = replace_non_space_white_characters(content)
                substantiation = extract_substantiation(content)
                if substantiation is not None:
                    replace_and_add_to_dict(replace_n, substantiation, judgements_by_type, case_label)


def replace_and_add_to_dict(replace_n: int, substantiation: str, judgements_by_type, case_label: str) -> None:
    top_words = read_top_n_words(replace_n)
    substantiation = replace_top_n_words(top_words, substantiation)
    substantiation = replace_redundant_characters(substantiation)
    substantiation = replace_digits(substantiation)
    substantiation = replace_single_letters(substantiation)
    substantiation = replace_multiple_white_characters(substantiation)
    substantiation = substantiation.lstrip().rstrip()
    judgements_by_type[case_label].append(substantiation)


if __name__ == '__main__':
    main()
