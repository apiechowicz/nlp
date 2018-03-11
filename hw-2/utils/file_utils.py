from os.path import join

JSONS_DIRECTORY = r'jsons'
CREATE_ANALYZER_JSON = r'2-create-analyzer.json'
CREATE_INDEX_JSON = r'3-create-index.json'


def get_create_analyzer_json(working_dir: str) -> str:
    return __read_json_file_to_string(join(working_dir, JSONS_DIRECTORY, CREATE_ANALYZER_JSON))


def get_create_index_json(working_dir: str) -> str:
    return __read_json_file_to_string(join(working_dir, JSONS_DIRECTORY, CREATE_INDEX_JSON))


def __read_json_file_to_string(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read().replace('\n', '')
