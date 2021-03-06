from typing import Tuple

from requests import post
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from tqdm import tqdm

from utils.argument_parser import parse_arguments
from utils.file_utils import extract_judgements_from_given_year_from_file, get_absolute_path, read_top_n_words, \
    save_data, append_to_output_file, create_output_file, get_files_to_be_processed
from utils.regex_utils import *

HOST = r'http://localhost:9200'
HEADERS = {'content-type': 'text/plain', 'charset': 'utf-8'}
ENCODING = r'utf-8'


def main():
    input_dir, judgement_year, replace_n, teaching_data_percentage = parse_arguments()
    files = get_files_to_be_processed(input_dir)
    judgements_by_type, tagged_judgements_by_type = group_judgements_by_type(files, input_dir, judgement_year,
                                                                             replace_n)
    # judgements_by_type, tagged_judgements_by_type = read_data(False), read_data(True)
    create_output_file()
    create_classifiers_and_evaluate(judgements_by_type, teaching_data_percentage, False)
    create_classifiers_and_evaluate(tagged_judgements_by_type, teaching_data_percentage, True)


def group_judgements_by_type(files, input_dir, judgement_year, replace_n):
    judgements_by_type = get_judgements_by_type_dict()
    tagged_judgements_by_type = get_judgements_by_type_dict()
    for file in tqdm(files, unit='files'):
        extract_judgements_from_file(file, input_dir, judgement_year, judgements_by_type, tagged_judgements_by_type,
                                     replace_n)
    save_data(judgements_by_type, False)
    save_data(tagged_judgements_by_type, True)
    return judgements_by_type, tagged_judgements_by_type


def get_judgements_by_type_dict() -> Dict[str, List[str]]:
    judgements_by_type = dict()
    for label in ALL_LABELS:
        judgements_by_type[label] = []
    return judgements_by_type


def extract_judgements_from_file(file: str, input_dir: str, judgement_year: int,
                                 judgements_by_type: Dict[str, List[str]],
                                 tagged_judgements_by_type: Dict[str, List[str]], replace_n: int) -> None:
    judgements = extract_judgements_from_given_year_from_file(get_absolute_path(file, input_dir), judgement_year)
    for judgement in judgements:
        if is_common_or_supreme_court_judgement(judgement):
            case_label = get_case_label(judgement)
            if case_label is not None:
                content = extract_from_judgement(judgement, 'textContent')
                content = replace_non_space_white_characters(content)
                substantiation = extract_substantiation(content)
                if substantiation is not None:
                    replace_and_add_to_dicts(replace_n, substantiation, judgements_by_type, tagged_judgements_by_type,
                                             case_label)


def replace_and_add_to_dicts(replace_n: int, substantiation: str, judgements_by_type, tagged_judgements_by_type,
                             case_label: str) -> None:
    top_words = read_top_n_words(replace_n)
    substantiation = substantiation.lower()
    substantiation = replace_top_n_words(top_words, substantiation)
    substantiation = replace_redundant_characters(substantiation)
    substantiation = replace_digits(substantiation)
    substantiation = replace_single_letters(substantiation)
    substantiation = replace_multiple_white_characters(substantiation)
    substantiation = substantiation.lstrip().rstrip()
    judgements_by_type[case_label].append(substantiation)
    tagged_substantiation = tagg_substantiation(substantiation)
    tagged_judgements_by_type[case_label].append(tagged_substantiation)


def tagg_substantiation(substantiation: str) -> str:
    response = post(url=HOST, headers=HEADERS, data=substantiation.encode(ENCODING))
    response_data = response.content.decode(ENCODING)
    words = []
    for line in response_data.split('\n'):
        if ':' in line:
            word = line.strip().replace('\t', ':').split(':')[0]
            words.append(word)
    return ' '.join(words)


def create_classifiers_and_evaluate(judgements_by_type: Dict[str, List[str]], teaching_data_percentage: int,
                                    tagged: bool) -> None:
    unit = 'labels (tagged)' if tagged else 'labels'
    for label in tqdm(sorted([l for l in judgements_by_type.keys()]), unit=unit):
        teaching_data_x, teaching_data_y, testing_data_x, testing_data_y = split_data_sets(judgements_by_type,
                                                                                           teaching_data_percentage,
                                                                                           label)
        if len(set(teaching_data_y)) > 1 and len(set(teaching_data_y)) > 1:
            clf = create_binary_tf_idf_classifier()
            clf.fit(teaching_data_x, teaching_data_y)
            clf = clf.best_estimator_
            predictions = clf.predict(testing_data_x)
            report = classification_report(testing_data_y, predictions)
            micro = precision_recall_fscore_support(testing_data_y, predictions, average='micro')
            macro = precision_recall_fscore_support(testing_data_y, predictions, average='macro')
            append_to_output_file(label, tagged, report, micro, macro)


def split_data_sets(judgements_by_type: Dict[str, List[str]], learning_data_percentage: int, classifier_label: str) \
        -> Tuple[List[str], List[str], List[str], List[str]]:
    teaching_data_x, teaching_data_y = [], []
    testing_data_x, testing_data_y = [], []
    for label in judgements_by_type.keys():
        data = judgements_by_type[label]
        data_size = len(data)
        if data_size > 2:
            learning_data_size = round(learning_data_percentage * data_size / 100)
            if data_size - learning_data_size < 1:
                learning_data_size -= 1
            classification = classifier_label if label == classifier_label else 'non-' + classifier_label
            add_data_to_sets(data[:learning_data_size], teaching_data_x, teaching_data_y, classification)
            add_data_to_sets(data[learning_data_size:], testing_data_x, testing_data_y, classification)
    return teaching_data_x, teaching_data_y, testing_data_x, testing_data_y


def add_data_to_sets(data, data_x, data_y, label):
    data_x.extend(data)
    data_y.extend([label for i in range(0, len(data))])


def create_binary_tf_idf_classifier() -> GridSearchCV:
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LinearSVC())
    ])
    parameters = {
        'tfidf__max_df': ([1 / 100] + list(x / 100 for x in range(5, 101, 5))),
        "clf__C": [0.01, 0.1, 1, 10, 100],
        "clf__class_weight": ['balanced', None]
    }
    return GridSearchCV(pipeline, parameters, n_jobs=4)


if __name__ == '__main__':
    main()
