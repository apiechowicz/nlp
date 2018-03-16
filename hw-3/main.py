from operator import itemgetter

from tqdm import tqdm

from utils.argument_parser import *
from utils.file_utils import *
from utils.regex_utils import replace_all_redundant_characters


def main():
    input_dir, judgement_year = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    results = process_data(files, judgement_year)
    results = sort_dictionary(results)
    save_data(results, 'exercise-2.txt')
    results = read_data('exercise-2.txt')
    print(results)


def process_data(files: List[str], judgement_year: int) -> Dict[str, int]:
    words_with_number_of_occurrences = dict()
    for file in tqdm(files, mininterval=15, unit='files'):
        judgements = extract_judgements_from_given_year_from_file(file, judgement_year)
        for judgement in judgements:
            content = extract_from_judgement(judgement, 'textContent')
            content = replace_all_redundant_characters(content)
            for word in content.split():
                if is_not_a_number(word) and is_a_word(word):
                    update_dictionary(words_with_number_of_occurrences, word)
    return words_with_number_of_occurrences


def update_dictionary(words_with_number_of_occurrences: Dict[str, int], word: str) -> None:
    try:
        words_with_number_of_occurrences[word] += 1
    except KeyError:
        words_with_number_of_occurrences[word] = 1


def sort_dictionary(results):
    return sorted(results.items(), key=itemgetter(1), reverse=True)


if __name__ == '__main__':
    main()
