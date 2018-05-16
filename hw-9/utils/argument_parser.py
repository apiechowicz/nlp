from argparse import ArgumentParser
from typing import Tuple


def parse_arguments() -> Tuple[str, int]:
    parser = ArgumentParser()
    parser.add_argument("input_dir", help="directory containing data to be processed")
    parser.add_argument("minimum_data_size", help="minimum size of text data in megabytes")
    args = parser.parse_args()
    return args.input_dir, int(args.minimum_data_size)
