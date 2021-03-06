from math import log2
from operator import itemgetter

from tqdm import tqdm

from utils.argument_parser import *
from utils.file_utils import *
from utils.regex_utils import replace_all_redundant_characters


def main():
    input_dir, judgement_year = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    unigram_frequency_list = process_data(files, judgement_year, True)
    save_data(unigram_frequency_list, 'exercise-1.txt')
    # unigram_frequency_list = read_data('exercise-1.txt')
    bigram_frequency_list = process_data(files, judgement_year, False)
    save_data(bigram_frequency_list, 'exercise-2.txt')
    # bigram_frequency_list = read_data('exercise-2.txt')
    pmi_list = create_pmi_list(unigram_frequency_list, bigram_frequency_list)
    save_data(pmi_list, 'exercise-3-4-5.txt')
    # pmi_list = read_data('exercise-3-4-5.txt')
    llr_list = create_llr_list(bigram_frequency_list)
    save_data(llr_list, 'exercise-6-7.txt')
    # llr_list = read_data('exercise-6-7.txt')


def process_data(files: List[str], judgement_year: int, process_single: bool) -> List[Tuple[str, int]]:
    words_with_number_of_occurrences = dict()
    for file in tqdm(files, mininterval=15, unit=' files'):
        judgements = extract_judgements_from_given_year_from_file(file, judgement_year)
        for judgement in judgements:
            content = extract_from_judgement(judgement, 'textContent')
            content = replace_all_redundant_characters(content)
            content = content.split()
            if process_single:
                count_single_words_in_content(content, words_with_number_of_occurrences)
            else:
                count_double_words_in_content(content, words_with_number_of_occurrences)
    return sort_dictionary(words_with_number_of_occurrences)


def count_single_words_in_content(content: List[str], words_with_number_of_occurrences: Dict[str, int]) -> None:
    for word in content:
        if is_not_a_number(word) and is_a_word(word):
            update_dictionary(words_with_number_of_occurrences, word.lower())


def update_dictionary(words_with_number_of_occurrences: Dict[str, int], word: str) -> None:
    try:
        words_with_number_of_occurrences[word] += 1
    except KeyError:
        words_with_number_of_occurrences[word] = 1


def count_double_words_in_content(content: List[str], words_with_number_of_occurrences: Dict[str, int]) -> None:
    for i in range(1, len(content)):
        phrase = content[i - 1:i + 1]
        is_phrase = True
        for word in phrase:
            if not is_not_a_number(word) or not is_a_word(word):
                is_phrase = False
                break
        if is_phrase:
            update_dictionary(words_with_number_of_occurrences, ' '.join(phrase).lower())


def sort_dictionary(results: Dict[str, int]) -> List[Tuple[str, int]]:
    return sorted(results.items(), key=itemgetter(1), reverse=True)


def create_pmi_list(unigram_frequency_list: List[Tuple[str, int]],
                    bigram_frequency_list: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    unigram_dict = convert_ngram_list_to_dict(unigram_frequency_list)
    unigram_total_words = sum_occurrences_in_ngram_frequency_list(unigram_frequency_list)
    bigram_total_words = sum_occurrences_in_ngram_frequency_list(bigram_frequency_list)
    pmi_list = []
    for phrase, occurrences in tqdm(bigram_frequency_list, mininterval=15, unit=' bigrams'):
        x, y = phrase.split(' ')
        px = unigram_dict[x] / unigram_total_words
        py = unigram_dict[y] / unigram_total_words
        pxy = occurrences / bigram_total_words
        pmi = log2(pxy / (px * py))
        pmi_list.append((phrase, pmi))
    return sorted(pmi_list, key=itemgetter(1), reverse=True)


def convert_ngram_list_to_dict(ngram_frequency_list: List[Tuple[str, int]]) -> Dict[str, int]:
    return {ngram: occurrences for ngram, occurrences in ngram_frequency_list}


def sum_occurrences_in_ngram_frequency_list(ngram_frequency_list: List[Tuple[str, int]]) -> int:
    return sum(occurrences for phrase, occurrences in ngram_frequency_list)


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


if __name__ == '__main__':
    main()
