from utils.argument_parser import parse_input_dir_argument
from utils.file_utils import get_files_to_be_processed, get_absolute_path, extract_judgements_from_given_year_from_file


def main() -> None:
    input_dir, judgement_year = parse_input_dir_argument()
    files_to_be_processed = get_files_to_be_processed(input_dir)
    for filename in files_to_be_processed:
        file = get_absolute_path(input_dir, filename)
        judgements_to_be_processed = extract_judgements_from_given_year_from_file(file, judgement_year)
        for judgement in judgements_to_be_processed:
            pass


if __name__ == '__main__':
    main()
