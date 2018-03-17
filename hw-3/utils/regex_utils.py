from datetime import datetime
from re import fullmatch, sub, search
from typing import Dict

INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = r'%Y-%m-%d'


def is_valid_input_file(filename: str) -> bool:
    return fullmatch(INPUT_FILE_NAME_PATTERN, filename) is not None


def get_judgement_date(judgement: Dict[str, str]) -> str:
    return judgement["judgmentDate"]


def extract_from_judgement(judgement: Dict[str, str], field_name: str):
    return judgement[field_name]


def judgement_year_matches(date: str, year: int) -> bool:
    return datetime.strptime(date, JUDGEMENT_DATE_FORMAT).year == year


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
    return fullmatch('\w{2,}', string) is not None and not string == string.upper()
