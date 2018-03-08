from argparse import ArgumentParser
from typing import Tuple


def parse_arguments() -> Tuple[str, int, int]:
    parser = ArgumentParser()
    parser.add_argument("input_dir", help="directory containing data to be processed")
    parser.add_argument("judgement_year", help="year for which judgements will be processed")
    parser.add_argument("dividing_point", help="number that will divide data for exercise 2")
    args = parser.parse_args()
    return args.input_dir, int(args.judgement_year), int(args.dividing_point)
