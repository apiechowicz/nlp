from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import get_files_to_be_processed, extract_judgements_from_given_year_from_file, save_data, \
    read_data
from utils.regex_utils import replace_redundant_characters


def main():
    input_dir, judgement_year, n = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    judgements = []
    for file in tqdm(files, unit='files'):
        judgements.extend(extract_judgements_from_given_year_from_file(file, judgement_year))
    judgements = sort_and_take_n_judgements(judgements, n)
    save_data(judgements, 'data.txt')
    judgements = read_data('data.txt')


def sort_and_take_n_judgements(judgements, n):
    sorted_judgements = [replace_redundant_characters(judgement['textContent']) for judgement
                         in sorted(judgements, key=lambda judgement: judgement['judgmentDate'])]
    return sorted_judgements[:n]


if __name__ == '__main__':
    main()
