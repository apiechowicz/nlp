from argparse import ArgumentParser
from typing import Tuple


def parse_arguments() -> Tuple[str, int, int, int]:
    parser = ArgumentParser()
    parser.add_argument("input_dir", help="directory containing data to be processed")
    parser.add_argument("judgement_year", help="year for which judgements will be processed")
    parser.add_argument("replace_n", help="percentage of data that should be used as test data")
    parser.add_argument("test_data_percentage", help="percentage of data that should be used as test data")
    args = parser.parse_args()
    return args.input_dir, int(args.judgement_year), int(args.replace_n), int(args.test_data_percentage)
