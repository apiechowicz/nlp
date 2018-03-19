from argparse import ArgumentParser
from typing import Tuple


def parse_arguments() -> Tuple[str, int, str, int]:
    parser = ArgumentParser()
    parser.add_argument("input_dir", help="directory containing data to be processed")
    parser.add_argument("judgement_year", help="year for which judgements will be processed")
    parser.add_argument("dict_path", help="path to dictionary file")
    parser.add_argument("number_of_words", help="number of words to be shown from words that are not in dictionary")
    args = parser.parse_args()
    return args.input_dir, int(args.judgement_year), args.dict_path, int(args.number_of_words)
