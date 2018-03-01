from argparse import ArgumentParser


def parse_input_dir_argument() -> str:
    parser = ArgumentParser()
    parser.add_argument("input_dir", help="directory containing data to be processed")
    args = parser.parse_args()
    return args.input_dir
