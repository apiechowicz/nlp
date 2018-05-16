from re import fullmatch, sub

INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'


def is_valid_input_file(filename: str) -> bool:
    return fullmatch(INPUT_FILE_NAME_PATTERN, filename) is not None


def replace_redundant_characters(content: str) -> str:
    content = replace_non_space_white_characters(content)
    content = replace_html_tags(content)
    content = replace_punctuation_marks(content)
    content = replace_multiple_white_characters(content)
    return content


def replace_non_space_white_characters(content: str) -> str:
    content = content.replace('-\n', ' ')
    content = content.replace('\n', ' ')
    content = content.replace('\t', ' ')
    return content


def replace_html_tags(content: str) -> str:
    content = sub("<[^>]*>", "", content)
    return content


def replace_punctuation_marks(content: str) -> str:
    content = sub('[§;:()\[\]"\'„…”/]', '', content)
    content = sub(' - ', ' ', content)
    return content


def replace_multiple_white_characters(content: str) -> str:
    return sub('\s{2,}', ' ', content)
