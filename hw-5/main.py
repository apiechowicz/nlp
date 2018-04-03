from operator import itemgetter
from typing import List, Tuple, Dict

from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import get_files_to_be_processed, TAGGED_JUDGEMENTS_DIRECTORY, get_words_from_tagged_judgement, \
    save_data, extract_and_upload_data, is_valid_input_file
from utils.regex_utils import is_not_a_number, is_a_word

HOST = r'http://localhost:9200'
HEADERS = {'content-type': 'text/plain', 'charset': 'utf-8'}


def main():
    input_dir, judgement_year = parse_arguments()
    files = get_files_to_be_processed(input_dir, is_valid_input_file)
    for file in tqdm(files, mininterval=15, unit='files'):
        extract_and_upload_data(file, judgement_year, HOST, HEADERS)
    judgement_files = get_files_to_be_processed(TAGGED_JUDGEMENTS_DIRECTORY, lambda x: True)
    bigram_frequency_list = create_bigram_list(judgement_files)
    save_data(bigram_frequency_list, 'exercise-3-4.txt')
    # bigram_frequency_list = read_data('exercise-3-4.txt')


def create_bigram_list(judgement_files: List[str]) -> List[Tuple[str, int]]:
    words_with_number_of_occurrences = dict()
    for file_path in tqdm(judgement_files, mininterval=15, unit='judgement-files'):
        words = get_words_from_tagged_judgement(file_path)
        for i in range(1, len(words)):
            phrase = words[i - 1:i + 1]
            is_phrase = True
            for word in phrase:
                if not is_not_a_number(word.split(':')[0]) or not is_a_word(word.split(':')[0]):
                    is_phrase = False
                    break
            if is_phrase:
                update_dictionary(words_with_number_of_occurrences, ' '.join(phrase).lower())
    return sort_dictionary(words_with_number_of_occurrences)


def update_dictionary(words_with_number_of_occurrences: Dict[str, int], word: str) -> None:
    try:
        words_with_number_of_occurrences[word] += 1
    except KeyError:
        words_with_number_of_occurrences[word] = 1


def sort_dictionary(results: Dict[str, int]) -> List[Tuple[str, int]]:
    return sorted(results.items(), key=itemgetter(1), reverse=True)


if __name__ == '__main__':
    main()
