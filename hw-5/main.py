from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import get_files_to_be_processed, extract_and_upload_data

HOST = r'http://localhost:9200'
HEADERS = {'content-type': 'text/plain', 'charset': 'utf-8'}


def main():
    input_dir, judgement_year = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    for file in tqdm(files, mininterval=15, unit='files'):
        extract_and_upload_data(file, judgement_year, HOST, HEADERS)


if __name__ == '__main__':
    main()
