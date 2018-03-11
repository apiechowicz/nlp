JSONS_DIRECTORY = r'jsons'
CREATE_ANALYZER_JSON = r'2-create-analyzer.json'


def read_json_to_string(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read().replace('\n', '')
