from re import sub, search, fullmatch

NOUN = r'subst'
ADJECTIVE = r'(\badj[apc]*\b)'


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


def is_noun(string: str):
    return fullmatch(NOUN, __get_flexeme_abbreviation(string)) is not None


def __get_flexeme_abbreviation(string: str) -> str:
    return string.split(':')[1]


def is_adjective(string: str):
    return fullmatch(ADJECTIVE, __get_flexeme_abbreviation(string)) is not None
