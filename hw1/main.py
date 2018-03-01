from utils.argument_parser import parse_input_dir_argument
from utils.file_utils import get_files_to_be_processed, get_absolute_path


def main() -> None:
    input_dir = parse_input_dir_argument()
    files_to_be_processed = get_files_to_be_processed(input_dir)
    for filename in files_to_be_processed:
        print(get_absolute_path(input_dir, filename))


if __name__ == '__main__':
    main()
