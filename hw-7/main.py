import sys
from os import devnull
from os import getcwd
from os.path import join
from typing import List

from utils.file_utils import save_data

sys.path.insert(0, join(getcwd(), 'pywnxml'))  # needed so that imports work in downloaded repository
from pywnxml.WNQuery import WNQuery
from utils.argument_parser import parse_arguments


def main():
    wordnet_file_path = parse_arguments()
    wn = WNQuery(wordnet_file_path, open(devnull, "w"))
    result = find_word(wn, 'szkoda', 'n')
    save_data(result, 'exercise-1-3.txt')
    result = find_relation(wn, 'wypadek', 1, 'n', 'hyponym', 1)  # shouldn't it be 'Hipo_plWN-PWN' or maybe both?
    save_data(result, 'exercise-5.txt')
    result2 = find_relation(wn, 'wypadek', 1, 'n', 'hyponym', 2)
    save_data(result2, 'exercise-6.txt')


def find_word(wn, word: str, word_type: str) -> str:
    results = wn.lookUpLiteral(word, word_type)
    output = ''
    if len(results) == 0:
        return 'Word {} with type {} has not been found.'.format(word, word_type)
    output += 'Queried word: {}\n'.format(word)
    output += 'Word type: {}\n'.format(word_type)
    output += 'Results:\n'
    for result in results:
        output += '\nDomain: {}\n'.format(result.domain)
        output += 'Definition: {}\n'.format(result.definition)
        output += 'Synonyms: '
        if len(result.synonyms) == 0:
            output += 'No synonyms have been found.'
        else:
            output += ', '.join([synonym.literal for synonym in result.synonyms])
        output += '\n'
    return output


def find_word_id(wn, word, sense_level, word_type):
    found_word = wn.lookUpSense(word, sense_level, word_type)
    return found_word.wnid


def find_relation(wn, word: str, semnum: int, word_type: str, relation_name: str, relation_depth_level: int) -> str:
    word_id = find_word_id(wn, word, semnum, word_type)
    output = 'Words that are in relation {} (relation level: {}) with word {}:\n'.format(relation_name,
                                                                                         relation_depth_level, word)
    words = find_words_in_relation(wn, word_id, relation_name, relation_depth_level)
    output += ', '.join(words)
    return output


def find_words_in_relation(wn, word_id: str, relation_name: str, relation_depth_level: int) -> List[str]:
    words_in_relation = wn.lookUpRelation(word_id, word_id[-1:], relation_name)
    words = []
    for synset_id in words_in_relation:
        if relation_depth_level == 1:
            synset = wn.lookUpID(synset_id, synset_id[-1:])
            words.extend([synonym.literal for synonym in synset.synonyms])
        else:
            words.extend(find_words_in_relation(wn, synset_id, relation_name, relation_depth_level - 1))
    return words


if __name__ == '__main__':
    main()
