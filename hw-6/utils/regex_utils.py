from datetime import datetime
from re import fullmatch, sub, search, split, IGNORECASE
from typing import Dict, List

INPUT_FILE_NAME_PATTERN = r'judgments-\d+\.json'
JUDGEMENT_DATE_FORMAT = r'%Y-%m-%d'

CIVIL_CASES_LABEL = r'civil'
INSURANCE_CASES_LABEL = r'insurance'
CRIMINAL_CASES_LABEL = r'criminal'
ECONOMIC_CASES_LABEL = r'economic'
LABOR_CASES_LABEL = r'labor'
FAMILY_CASES_LABEL = r'family'
OFFENSE_CASES_LABEL = r'offense'
COMPETITION_CASES_LABEL = r'competition'
ALL_LABELS = [CIVIL_CASES_LABEL, INSURANCE_CASES_LABEL, CRIMINAL_CASES_LABEL, ECONOMIC_CASES_LABEL, LABOR_CASES_LABEL,
              FAMILY_CASES_LABEL, OFFENSE_CASES_LABEL, COMPETITION_CASES_LABEL]

COURT_TYPES = ['COMMON', 'SUPREME']

SIGNATURE_REGEX_WITH_LABELS = {'A?C.*': CIVIL_CASES_LABEL, 'A?U.*': INSURANCE_CASES_LABEL,
                               'A?K.*': CRIMINAL_CASES_LABEL, 'G.*': ECONOMIC_CASES_LABEL, 'A?P.*': LABOR_CASES_LABEL,
                               'R.*': FAMILY_CASES_LABEL, 'W.*': OFFENSE_CASES_LABEL, 'Am.*': COMPETITION_CASES_LABEL}

SUBSTANTIATION_WORD = r'uzasadnienie'


def is_valid_input_file(filename: str) -> bool:
    return fullmatch(INPUT_FILE_NAME_PATTERN, filename) is not None


def judgement_year_matches(date: str, year: int) -> bool:
    return datetime.strptime(date, JUDGEMENT_DATE_FORMAT).year == year


def get_judgement_date(judgement: Dict[str, str]) -> str:
    return judgement["judgmentDate"]


def extract_from_judgement(judgement: Dict[str, str], field_name: str):
    return judgement[field_name]


def is_common_or_supreme_court_judgement(judgement: Dict[str, str]) -> bool:
    court_type = extract_from_judgement(judgement, 'courtType')
    return court_type in COURT_TYPES


def get_case_label(judgement: Dict[str, str]) -> str or None:
    court_cases = extract_from_judgement(judgement, 'courtCases')[0]
    signature = extract_from_judgement(court_cases, 'caseNumber')
    for regex in SIGNATURE_REGEX_WITH_LABELS.keys():
        if search(regex, signature):
            return SIGNATURE_REGEX_WITH_LABELS[regex]
    return None


def replace_non_space_white_characters(content: str) -> str:
    content = content.replace('-\n', ' ')
    content = content.replace('\n', ' ')
    content = content.replace('\t', ' ')
    return content


def extract_substantiation(content: str) -> str or None:
    if search(SUBSTANTIATION_WORD, content, IGNORECASE):
        return split(SUBSTANTIATION_WORD, content, 1, IGNORECASE)[1]
    return None


def replace_redundant_characters(content: str) -> str:
    content = sub("<[^>]*>", "", content)
    content = sub('[§,.;:\-–−()\[\]"\'„…”/]', "", content)
    return content


def replace_top_n_words(top_words: List[str], content: str) -> str:
    for word in top_words:
        content = sub('\s{}\s'.format(word), ' ', content)
    return content


def replace_digits(content: str) -> str:
    digits = [digit for digit in '0123456789']
    for digit in digits:
        content = sub(digit, '', content)
    return content


def replace_single_letters(content: str) -> str:
    letters = [letter for letter in 'aąbcćdeęfghijklłmnńoóprsśtuwzżź']
    for letter in letters:
        content = sub('\s{}\s'.format(letter), ' ', content)
    return content


def replace_multiple_white_characters(content: str) -> str:
    return sub('\s{2,}', ' ', content)
