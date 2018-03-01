from argparse import ArgumentParser
from typing import Tuple


def parse_input_dir_argument() -> Tuple[str, int]:
    parser = ArgumentParser()
    parser.add_argument("input_dir", help="directory containing data to be processed")
    parser.add_argument("judgement_year", help="year for which judgements will be processed")
    args = parser.parse_args()
    return args.input_dir, int(args.judgement_year)
