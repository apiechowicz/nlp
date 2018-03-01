from utils.argument_parser import parse_input_dir_argument
from utils.file_utils import get_files_to_be_processed, get_absolute_path, extract_judgements_from_given_year_from_file, \
    extract_judgement_content
from utils.regex_utils import find_money_in_string


def main() -> None:
    input_dir, judgement_year = parse_input_dir_argument()
    files_to_be_processed = get_files_to_be_processed(input_dir)
    for filename in files_to_be_processed:  # todo add tqdm progressbar
        file = get_absolute_path(input_dir, filename)
        judgements_to_be_processed = extract_judgements_from_given_year_from_file(file, judgement_year)
        for judgement in judgements_to_be_processed:
            content = extract_judgement_content(judgement)
            match = find_money_in_string(content)
            print(match)


if __name__ == '__main__':
    main()
