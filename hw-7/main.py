import sys
from os import getcwd
from os.path import join, devnull
from typing import List, Tuple, Dict

from networkx import DiGraph

sys.path.insert(0, join(getcwd(), 'pywnxml'))  # needed so that imports work in downloaded repository
from pywnxml.WNQuery import WNQuery
from utils.argument_parser import parse_arguments
from utils.file_utils import save_graph, save_data


def main():
    wordnet_file_path = parse_arguments()
    wn = WNQuery(wordnet_file_path, open(devnull, "w"))
    result = find_word(wn, 'szkoda', 'n')
    save_data(result, 'exercise-1-3.txt')
    result = find_relation(wn, 'wypadek', 1, 'n', 'hyponym', 1)  # shouldn't it be 'Hipo_plWN-PWN' or maybe both?
    save_data(result, 'exercise-5.txt')
    result2 = find_relation(wn, 'wypadek', 1, 'n', 'hyponym', 2)
    save_data(result2, 'exercise-6.txt')
    words_1 = [('szkoda', 2, 'n'), ('strata', 1, 'n'), ('uszczerbek', 1, 'n'), ('szkoda majątkowa', 1, 'n'),
               ('uszczerbek na zdrowiu', 1, 'n'), ('krzywda', 1, 'n'), ('niesprawiedliwość', 1, 'n'),
               ('nieszczęście', 2, 'n')]
    graph, edge_labels = create_relations_graph(wn, words_1)
    save_graph(graph, edge_labels, 'exercise-7-I.png')
    words_2 = [('wypadek', 1, 'n'), ('wypadek komunikacyjny', 1, 'n'), ('kolizja', 2, 'n'), ('zderzenie', 2, 'n'),
               ('kolizja drogowa', 1, 'n'),
               # ('bezkolizyjny', 2, 'j'), # todo this word is in j pos - WNQuery does not support j pos.
               ('katastrofa budowlana', 1, 'n'), ('wypadek drogowy', 1, 'n')]
    graph, edge_labels = create_relations_graph(wn, words_2)
    save_graph(graph, edge_labels, 'exercise-7-II.png')


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


def find_relation(wn, word: str, semnum: int, word_type: str, relation_name: str, relation_depth_level: int) -> str:
    word_id = find_word_id(wn, word, semnum, word_type)
    output = 'Words that are in relation {} (relation level: {}) with word {}:\n'.format(relation_name,
                                                                                         relation_depth_level, word)
    words = find_words_in_relation(wn, word_id, relation_name, relation_depth_level)
    output += ', '.join(words)
    return output


def find_word_id(wn, word, sense_level, word_type):
    found_word = wn.lookUpSense(word, sense_level, word_type)
    return found_word.wnid


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


def create_relations_graph(wn, words: List[Tuple[str, int, str]]) -> Tuple[DiGraph, Dict[Tuple[str, str], str]]:
    word_synset_pairs, synset_ids = [], []
    graph = DiGraph()
    for word in words:
        synset = wn.lookUpSense(*word)
        word_synset_pairs.append((word, synset))
        synset_ids.append(synset.wnid)
        graph.add_node(get_vertex_label(word))
    edge_labels = {}
    for word, synset in word_synset_pairs:
        synset.ilrs = [relation for relation in synset.ilrs if relation[0] in synset_ids]
        for id_of_synset_in_relation, relation_name in synset.ilrs:
            words_in_relation = get_words_in_synset_that_match(wn, id_of_synset_in_relation, words)
            for word_in_relation in words_in_relation:
                u = get_vertex_label(word)
                v = get_vertex_label(word_in_relation)
                graph.add_edge(u, v)
                edge_labels[(u, v)] = relation_name  # todo figure out how to use MultiDiGraph edges instead?
    return graph, edge_labels


def get_words_in_synset_that_match(wn, id_of_synset: str, words: List[Tuple[str, int, str]]) \
        -> List[Tuple[str, int, str]]:
    synset = wn.lookUpID(id_of_synset, id_of_synset[-1:])
    words_in_synset = []
    for synonym in synset.synonyms:
        for word in words:
            if word[0] == synonym.literal and str(word[1]) == synonym.sense:
                words_in_synset.append(word)
    return words_in_synset


def get_vertex_label(word: Tuple[str, int, str]) -> str:
    return '_'.join([str(part) for part in word][:2])


if __name__ == '__main__':
    main()
