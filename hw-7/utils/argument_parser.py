from argparse import ArgumentParser
from typing import Tuple


def parse_arguments() -> Tuple[str, int, int, int]:
    parser = ArgumentParser()
    parser.add_argument("wordnet_file_path", help="absolute path to file with wordnet data")
    args = parser.parse_args()
    return args.wordnet_file_path
