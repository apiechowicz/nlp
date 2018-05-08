import sys
from os import getcwd
from os.path import join, devnull
from typing import List, Tuple, Dict

from networkx import DiGraph, compose

sys.path.insert(0, join(getcwd(), 'pywnxml'))  # needed so that imports work in downloaded repository
from pywnxml.WNQuery import WNQuery
from utils.argument_parser import parse_arguments
from utils.file_utils import save_data, save_graph


def main():
    wordnet_file_path = parse_arguments()
    wn = WNQuery(wordnet_file_path, open(devnull, "w"))
    result = find_word(wn, 'szkoda', 'n')
    save_data(result, 'exercise-1-3.txt')
    graph, edge_labels = find_transitive_closure(wn, 'wypadek drogowy', 1, 'n', 'hypernym')
    save_graph(graph, edge_labels, 'exercise-4.png')
    result = find_relation(wn, 'wypadek', 1, 'n', 'hyponym', 1)
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


def find_transitive_closure(wn, word: str, sense_level: int, word_type: str, relation_name: str) \
        -> Tuple[DiGraph, Dict[Tuple[str, str], str]]:
    synset = wn.lookUpSense(word, sense_level, word_type)
    graph = DiGraph()
    edge_labels = {}
    u = get_vertex_label((word, sense_level, word_type))
    graph.add_node(u)
    for synset_id, relation in synset.ilrs:
        if relation == relation_name:
            synset_in_relation = wn.lookUpID(synset_id, synset_id[-1:])
            for word_in_relation in synset_in_relation.synonyms:
                word_in_relation_as_tuple = (word_in_relation.literal, int(word_in_relation.sense),
                                             synset_in_relation.pos)
                v = get_vertex_label(word_in_relation_as_tuple)
                graph.add_node(v)
                graph.add_edge(v, u)
                edge_labels[(u, v)] = relation_name
                sub_graph, sub_graph_edge_labels = find_transitive_closure(wn, *word_in_relation_as_tuple,
                                                                           relation_name)
                graph = compose(graph, sub_graph)
                edge_labels = {**edge_labels, **sub_graph_edge_labels}
    return graph, edge_labels


def get_vertex_label(word: Tuple[str, int, str]) -> str:
    return '_'.join([str(part) for part in word][:2])


def find_relation(wn, word: str, sense_level: int, word_type: str, relation_name: str,
                  relation_depth_level: int) -> str:
    word_id = find_word_id(wn, word, sense_level, word_type)
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
        add_synonym_relations(synset, word, words, edge_labels, graph)
        find_and_add_relations(synset, synset_ids, wn, words, word, graph, edge_labels)
    return graph, edge_labels


def add_synonym_relations(synset, word, words, edge_labels, graph):
    for synonym in synset.synonyms:
        if synonym.literal in [word[0] for word in words] and synonym.literal != word[0]:
            u = get_vertex_label(word)
            v = get_vertex_label((synonym.literal, int(synonym.sense), word[2]))
            graph.add_edge(u, v)
            edge_labels[(u, v)] = 'synonym'
            graph.add_edge(v, u)
            edge_labels[(v, u)] = 'synonym'


def find_and_add_relations(synset, synset_ids, wn, words, word, graph, edge_labels):
    synset.ilrs = [relation for relation in synset.ilrs if relation[0] in synset_ids]
    for id_of_synset_in_relation, relation_name in synset.ilrs:
        words_in_relation = get_words_in_synset_that_match(wn, id_of_synset_in_relation, words)
        for word_in_relation in words_in_relation:
            u = get_vertex_label(word)
            v = get_vertex_label(word_in_relation)
            graph.add_edge(u, v)
            edge_labels[(u, v)] = relation_name


def get_words_in_synset_that_match(wn, id_of_synset: str, words: List[Tuple[str, int, str]]) \
        -> List[Tuple[str, int, str]]:
    synset = wn.lookUpID(id_of_synset, id_of_synset[-1:])
    words_in_synset = []
    for synonym in synset.synonyms:
        for word in words:
            if word[0] == synonym.literal and str(word[1]) == synonym.sense:
                words_in_synset.append(word)
    return words_in_synset


if __name__ == '__main__':
    main()
