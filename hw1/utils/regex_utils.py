from datetime import datetime
from re import fullmatch, compile, IGNORECASE, findall

INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = r'%Y-%m-%d'
MONEY_PATTERN = r'(\d+(?:[ .,]?\d+)*(?: ?(?:tys\.|mln))?(?= ?(?:zł(?:ote|otych|(?!\w))|pln)))'


def is_valid_input_file(filename: str) -> bool:
    return fullmatch(INPUT_FILE_NAME_PATTERN, filename) is not None


def judgement_year_matches(date: str, year: int) -> bool:
    return datetime.strptime(date, JUDGEMENT_DATE_FORMAT).year == year


def find_money_in_string(judgement_content: str):
    pattern = compile(MONEY_PATTERN, IGNORECASE)
    return findall(pattern, judgement_content)
