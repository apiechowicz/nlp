from re import sub, search, fullmatch


def replace_all_redundant_characters(content: str) -> str:
    content = content.replace('-\n', ' ')
    content = content.replace('\n', ' ')
    content = content.replace('\t', ' ')
    content = sub("<[^>]*>", "", content)
    content = sub('[,.;:\-–−()\[\]"„…”/]', "", content)
    return content


def is_not_a_number(string: str):
    return search('\d', string) is None


def is_a_word(string: str):
    return fullmatch('\w+', string) is not None and not string == string.upper()
