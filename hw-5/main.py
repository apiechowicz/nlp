from math import log2
from operator import itemgetter
from typing import List, Tuple, Dict

from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import get_files_to_be_processed, TAGGED_JUDGEMENTS_DIRECTORY, get_words_from_tagged_judgement, \
    save_data, extract_and_upload_data, is_valid_input_file
from utils.regex_utils import is_not_a_number, is_a_word, is_noun, is_adjective

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
    llr_list = create_llr_list(bigram_frequency_list)
    save_data(llr_list, 'exercise-5.txt')
    # llr_list = read_data('exercise-5.txt')
    filtered_llr = filter_llr(llr_list)
    save_data(filtered_llr, 'exercise-6.txt')
    # filtered_llr = read_data('exercise-6.txt')


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


def create_llr_list(bigram_frequency_list: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    bigram_total_words = sum_occurrences_in_ngram_frequency_list(bigram_frequency_list)
    event_occurrences = count_event_occurrences(bigram_frequency_list)
    llr_list = []
    for phrase, occurrences in tqdm(bigram_frequency_list, mininterval=1, unit=' bigrams'):
        a, b = phrase.split(' ')
        k_11 = occurrences
        k_12 = event_occurrences[b][1] - occurrences
        k_21 = event_occurrences[a][0] - occurrences
        k_22 = bigram_total_words - k_11 - k_12 - k_21
        llr = 2 * (k_11 + k_12 + k_21 + k_22) * (entropy([k_11, k_12, k_21, k_22]) - entropy([k_11 + k_12, k_21 + k_22])
                                                 - entropy([k_11 + k_21, k_12 + k_22]))
        llr_list.append((phrase, llr))
    return sorted(llr_list, key=itemgetter(1), reverse=True)


def sum_occurrences_in_ngram_frequency_list(ngram_frequency_list: List[Tuple[str, int]]) -> int:
    return sum(occurrences for phrase, occurrences in ngram_frequency_list)


def count_event_occurrences(bigram_frequency_list: List[Tuple[str, int]]) -> Dict[str, Tuple[int, int]]:
    event_occurrences = dict()
    # word -> (number of occurrences as first element, number of occurrences as second element)
    for phrase, count in bigram_frequency_list:
        a, b = phrase.split(' ')
        try:
            event_occurrences[a] = (event_occurrences[a][0] + count, event_occurrences[a][1])
        except KeyError:
            event_occurrences[a] = (count, 0)
        try:
            event_occurrences[b] = (event_occurrences[b][0], event_occurrences[b][1] + count)
        except KeyError:
            event_occurrences[b] = (0, count)
    return event_occurrences


def entropy(items: List[int]) -> float:
    N = sum(items)
    return sum(nlogn(item, N) for item in items)


def nlogn(item: int, N: int):
    k_div_N = item / N
    return k_div_N * log2(k_div_N + int(item == 0))


def filter_llr(llr_list: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    filtered = []
    for phrase, count in llr_list:
        first_word, second_word = phrase.split(' ')
        if is_noun(first_word) and (is_noun(second_word) or is_adjective(second_word)):
            filtered.append((phrase, count))
    return filtered


if __name__ == '__main__':
    main()
