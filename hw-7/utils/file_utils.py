from os import getcwd, makedirs
from os.path import join, isdir

OUTPUT_DIRECTORY_NAME = r'out'
OUTPUT_DIRECTORY_PATH = join(getcwd(), OUTPUT_DIRECTORY_NAME)


def save_data(data: str, file_name: str) -> None:
    create_output_dir(OUTPUT_DIRECTORY_PATH)
    with open(join(OUTPUT_DIRECTORY_PATH, file_name), 'w') as file:
        file.write(data)


def create_output_dir(path: str) -> None:
    if not isdir(path):
        makedirs(path)
