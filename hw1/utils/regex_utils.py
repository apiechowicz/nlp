from datetime import datetime
from re import fullmatch, compile, IGNORECASE, findall

INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = r'%Y-%m-%d'
MONEY_PATTERN = r'(?:[1-9]\d*|0(?=,))(?:[ .,]?\d+)*(?: ?(?:tys\.|mln))?(?= ?(?:zł(?:ote|otych|(?!\w))|pln))'


def is_valid_input_file(filename: str) -> bool:
    return fullmatch(INPUT_FILE_NAME_PATTERN, filename) is not None


def judgement_year_matches(date: str, year: int) -> bool:
    return datetime.strptime(date, JUDGEMENT_DATE_FORMAT).year == year


def find_money_in_string(judgement_content: str):
    pattern = compile(MONEY_PATTERN, IGNORECASE)
    return findall(pattern, judgement_content)


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
    return number


def __replace_delimiters(number: str) -> str:
    number = number.replace(' ', '')
    number = number.replace('.', '')
    number = number.replace(',', '')
    return number
