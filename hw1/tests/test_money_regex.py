from itertools import product
from unittest import TestCase, main

from parameterized import parameterized

from hw1.utils.regex_utils import find_money_in_string


def generate_test_cases():
    amounts = ["1", "1 000", "1 000 000"]
    delimiters = [' ', '.', ',']
    white_char_before_currency = [True, False]
    currency = ["zł", "złote", "złotych", "pln"]
    to_upper_case = [True, False]
    combinations = product(amounts, delimiters, white_char_before_currency, currency, to_upper_case)
    return [__convert_test_case(comb) for comb in combinations]


def __convert_test_case(parameters):
    amount, delimiter, white_char_before_currency, currency, to_upper_case = parameters
    amount = amount.replace(' ', delimiter)
    currency = currency.upper() if to_upper_case else currency.lower()
    currency = ' ' + currency if white_char_before_currency else currency
    return amount + currency


class MoneyRegexTest(TestCase):
    @parameterized.expand([
        ("number with word starting with zł afterwards", "300 złowrogich"),
        ("number with no currency", "1000"),
        ("number with non Polish currency", "1000 eur"),
        ("number with non Polish currency", "1000 usd")
    ])
    def test_should_not_find(self, name, input):
        found = find_money_in_string(input)
        self.assertEqual(len(found), 0)

    @parameterized.expand(generate_test_cases())
    def test_should_find(self, input):
        found = find_money_in_string(input)
        self.assertEqual(len(found), 1)


if __name__ == '__main__':
    main()
