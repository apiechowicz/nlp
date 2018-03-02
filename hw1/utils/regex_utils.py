from datetime import datetime
from re import fullmatch, findall

INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = r'%Y-%m-%d'
MONEY_PATTERN = r'(\d+(?:[ .,]?\d+)*(?= ?zł(?:ote|otych|(?!\w))))'


# MONEY_PATTERN = r'(\d+(?:[ .,]?\d+)*(?= ?zł(?:ote|otych|(?!\w))))'
# todo add pln
# todo add currency upper and lowercase handling (ignore case in regex)
# todo add abbreviations like tys.


def is_valid_input_file(filename: str) -> bool:
    return fullmatch(INPUT_FILE_NAME_PATTERN, filename) is not None


def judgement_year_matches(date: str, year: int) -> bool:
    return datetime.strptime(date, JUDGEMENT_DATE_FORMAT).year == year


def find_money_in_string(judgement_content: str):
    return findall(MONEY_PATTERN, judgement_content)
