from operator import itemgetter

from matplotlib import pyplot
from tqdm import tqdm

from utils.argument_parser import *
from utils.file_utils import *
from utils.regex_utils import replace_all_redundant_characters


def main():
    input_dir, judgement_year, dict_path, number_of_words = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    results = process_data(files, judgement_year)
    results = sort_dictionary(results)
    save_data(results, 'exercise-2.txt')
    # results = read_data('exercise-2.txt')
    create_chart(results, 'exercise-4.png', judgement_year)
    not_in_dictionary = find_words_that_are_not_in_dictionary(dict_path, results)
    save_data(not_in_dictionary, 'exercise-5.txt')
    # not_in_dictionary = read_data('exercise-5.txt')
    print_only_number_of_words(not_in_dictionary, number_of_words)


def process_data(files: List[str], judgement_year: int) -> Dict[str, int]:
    words_with_number_of_occurrences = dict()
    for file in tqdm(files, mininterval=15, unit=' files'):
        judgements = extract_judgements_from_given_year_from_file(file, judgement_year)
        for judgement in judgements:
            content = extract_from_judgement(judgement, 'textContent')
            content = replace_all_redundant_characters(content)
            for word in content.split():
                if is_not_a_number(word) and is_a_word(word):
                    update_dictionary(words_with_number_of_occurrences, word.lower())
    return words_with_number_of_occurrences


def update_dictionary(words_with_number_of_occurrences: Dict[str, int], word: str) -> None:
    try:
        words_with_number_of_occurrences[word] += 1
    except KeyError:
        words_with_number_of_occurrences[word] = 1


def sort_dictionary(results):
    return sorted(results.items(), key=itemgetter(1), reverse=True)


def create_chart(data: List, filename: str, year: int):
    output_file = join(OUTPUT_DIRECTORY_PATH, filename)
    create_output_dir()
    x, y = prepare_data_for_plotting(data)
    # pyplot.semilogy(x, y)
    pyplot.loglog(x, y)
    pyplot.title('Number of word occurrences vs position on the\nfrequency list for words in judgements from {}'.format(
        str(year)))
    pyplot.xlabel('Index on the frequency list [log]')
    pyplot.ylabel('Number of word occurrences in judgements [log]')
    pyplot.grid(True)
    pyplot.savefig(output_file, dpi=150)
    pyplot.close()


def prepare_data_for_plotting(data) -> Tuple[List[int], List[int]]:
    y = list(item[1] for item in data)
    x = list(range(1, len(y) + 1))
    return x, y


def find_words_that_are_not_in_dictionary(dictionary_path: str, results: List[Tuple[str, int]]) -> List[str]:
    dictionary_data = read_dictionary_data(dictionary_path)
    not_in_dictionary = []
    for word, count in tqdm(results, mininterval=10, unit=' words'):
        bucket = word[:2].lower()
        try:
            if word not in dictionary_data[bucket]:
                not_in_dictionary.append(word)
        except KeyError:
            not_in_dictionary.append(word)
    return not_in_dictionary


def print_only_number_of_words(not_in_dictionary: List[str],
                               number_of_words: int) -> None:
    if number_of_words > len(not_in_dictionary):
        print('There are only {} words that are not in dictionary.'.format(len(not_in_dictionary)))
        print(not_in_dictionary)
    else:
        print(not_in_dictionary[:number_of_words])


if __name__ == '__main__':
    main()
