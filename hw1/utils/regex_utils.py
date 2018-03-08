from datetime import datetime
from re import fullmatch, compile, IGNORECASE, findall, search

INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = r'%Y-%m-%d'
MONEY_PATTERN = r'(?:[1-9]\d*|0(?=,))(?:[ .,]?\d+)*(?: ?(?:tys\.|mln|mld))?(?= ?(?:zł(?:ote|otych|(?!\w))|pln))'
DETRIMENT_PATTERN = r'(\bszk(?:od(?:ami|ach|a|y|zie|ę|ą|om|o)|ód)\b)'
LAW_NAME = r'Ustawa z dnia 23 kwietnia 1964 r. - Kodeks cywilny'
ARTICLE_PATTERN = r'(art(?:\.|ykuł\w{0,3}|ykule) 445)'


def is_valid_input_file(filename: str) -> bool:
    return fullmatch(INPUT_FILE_NAME_PATTERN, filename) is not None


def judgement_year_matches(date: str, year: int) -> bool:
    return datetime.strptime(date, JUDGEMENT_DATE_FORMAT).year == year


def find_pattern_in_string(pattern: str, string: str):
    pattern = compile(pattern, IGNORECASE)
    return findall(pattern, string)


def convert_money_string_to_int(number: str) -> int:
    number = __skip_grosze(number)
    number = __replace_abbreviations(number)
    number = __replace_delimiters(number)
    return int(number)


def __skip_grosze(number: str) -> str:
    number_tuple = number.rsplit(',', 1)
    if len(number_tuple) == 2 and len(number_tuple[1]) == 2:
        return number_tuple[0]
    return number


def __replace_abbreviations(number: str) -> str:
    number = number.replace('tys.', 3 * '0')
    number = number.replace('mln', 6 * '0')
    number = number.replace('mld', 9 * '0')
    return number


def __replace_delimiters(number: str) -> str:
    number = number.replace(' ', '')
    number = number.replace('.', '')
    number = number.replace(',', '')
    return number


def find_pattern_once_in_string(pattern: str, string: str):
    pattern = compile(pattern, IGNORECASE)
    return search(pattern, string)
