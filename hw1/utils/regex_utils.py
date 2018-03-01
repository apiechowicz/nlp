from datetime import datetime
from re import fullmatch

INPUT_FILE_NAME_PATTERN = 'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = '%Y-%m-%d'


def is_valid_input_file(filename: str) -> bool:
    return fullmatch(INPUT_FILE_NAME_PATTERN, filename) is not None


def judgement_year_matches(date: str, year: int) -> bool:
    return datetime.strptime(date, JUDGEMENT_DATE_FORMAT).year == year
