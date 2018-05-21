from gc import collect
from os import listdir
from os.path import getsize, basename, join
from typing import List

from gensim.models import Phrases, Word2Vec
from gensim.models.phrases import Phraser
from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import get_files_to_be_processed, extract_judgements_from_file, save_data, \
    PREPROCESSED_DATA_DIRECTORY_PATH, read_data, TRIGRAMS_DATA_DIRECTORY_PATH, OUTPUT_DIRECTORY_PATH
from utils.regex_utils import replace_redundant_characters, extract_sentences

BYTES_IN_MEGABYTE = 1024 * 1024


def main():
    input_dir, minimum_data_size = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    files = select_random_files(files, minimum_data_size)
    preprocessed_files = preprocess_judgements(files)
    trigram_files = convert_to_trigram_sentences(preprocessed_files)
    # trigram_files = convert_to_trigram_sentences(listdir(PREPROCESSED_DATA_DIRECTORY_PATH))
    model = create_model(trigram_files)
    # model = create_model(listdir(TRIGRAMS_DATA_DIRECTORY_PATH))
    model.save(join(OUTPUT_DIRECTORY_PATH, 'trigrams.model'))
    model = Word2Vec.load(join(OUTPUT_DIRECTORY_PATH, 'trigrams.model'))
    results = find_n_most_similar(model, 3,
                                  ['Sąd Najwyższy', 'Trybunał Konstytucyjny', 'kodeks cywilny', 'kpk', 'sąd rejonowy',
                                   'szkoda', 'wypadek', 'kolizja', 'szkoda majątkowa', 'nieszczęście', 'rozwód'])
    save_data(OUTPUT_DIRECTORY_PATH, results, 'exercise-7.txt')


def preprocess_judgements(files: List[str]) -> List[str]:
    file_names = []
    for file in tqdm(files, unit='judgement files'):
        judgements = extract_judgements_from_file(file)
        judgements = [replace_redundant_characters(judgement["textContent"]) for judgement in judgements]
        file_name = basename(file).replace('.json', '.txt')
        save_data(PREPROCESSED_DATA_DIRECTORY_PATH, judgements, file_name)
        file_names.append(file_name)
    return file_names


def select_random_files(files: List[str], minimum_data_size: float) -> List[str]:
    total_size = get_total_size_in_megabytes(files)
    division_point = get_division_point(total_size, minimum_data_size)
    return files[:int(len(files) / division_point)]


def get_total_size_in_megabytes(files: List[str]) -> float:
    return sum([getsize(file) for file in files]) / BYTES_IN_MEGABYTE


def get_division_point(total_size: float, minimum_data_size: float) -> int:
    divider = 1
    while total_size / (divider + 1) > minimum_data_size:
        divider += 1
    return divider + 1 if total_size / divider + 1 >= 0.9 * minimum_data_size else divider


def convert_to_trigram_sentences(preprocessed_files_file_names: List[str]) -> List[str]:
    for file_name in tqdm(preprocessed_files_file_names, unit='preprocessed files'):
        judgements = read_data(PREPROCESSED_DATA_DIRECTORY_PATH, file_name)
        sentences_stream = convert_to_sentences_stream(judgements)
        phrases = Phrases(sentences_stream)
        bigram = Phraser(phrases)
        trigram = Phrases(bigram[sentences_stream])
        trigram_phrases = [trigram[bigram[sentence]] for sentence in sentences_stream]
        trigram_sentences = [' '.join(trigrams) for trigrams in trigram_phrases]
        save_data(TRIGRAMS_DATA_DIRECTORY_PATH, trigram_sentences, file_name)
    return preprocessed_files_file_names


def convert_to_sentences_stream(judgements):
    sentences_stream = []
    for judgement in judgements:
        sentences = extract_sentences(judgement)
        for sentence in sentences:
            sentences_stream.append(convert_to_stream(sentence))
    return sentences_stream


def convert_to_stream(sentence: str) -> List[str]:
    return sentence.lower().replace('.', '').replace(',', '').split(' ')


def create_model(trigram_files: List[str]):
    sentences = []
    for file_name in tqdm(trigram_files, unit='trigram files'):
        trigram_sentences = read_data(TRIGRAMS_DATA_DIRECTORY_PATH, file_name)
        for sentence in trigram_sentences:
            sentences.append(sentence.split(' '))
        collect()
    print('Training started')
    model = Word2Vec(sentences, sg=0, window=5, size=300, min_count=3, workers=4)
    print('Training finished')
    return model


def find_n_most_similar(model: Word2Vec, top_n: int, words: List[str]) -> List[str]:
    results = []
    for word in words:
        most_similar = model.wv.most_similar(positive=word.lower().replace(' ', '_'), topn=top_n)
        result = '{} most similar words to word {} are:\n'.format(top_n, word)
        result += '\n'.join(['{} - similarity: {}'.format(result_word, round(similarity, 4))
                             for result_word, similarity in most_similar])
        results.append(result)
    return results


if __name__ == '__main__':
    main()
