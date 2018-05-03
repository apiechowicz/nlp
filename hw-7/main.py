import sys
from os import devnull
from os import getcwd
from os.path import join

from utils.file_utils import save_data

sys.path.insert(0, join(getcwd(), 'pywnxml'))  # needed so that imports work in downloaded repository
from pywnxml.WNQuery import WNQuery
from utils.argument_parser import parse_arguments


def main():
    wordnet_file_path = parse_arguments()
    wn = WNQuery(wordnet_file_path, open(devnull, "w"))
    result = find_word(wn, "szkoda", "n")
    save_data(result, 'exercise-1-3.txt')


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


if __name__ == '__main__':
    main()
