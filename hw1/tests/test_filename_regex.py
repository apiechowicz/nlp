from unittest import TestCase, main

from hw1.utils.regex_utils import is_valid_input_file


class FileNameRegexTest(TestCase):
    def test_courts_data_should_not_be_valid(self):
        is_valid = is_valid_input_file("courts-1.json")
        self.assertEqual(is_valid, False)

    def test_judgements_file_with_no_extension_should_not_be_valid(self):
        is_valid = is_valid_input_file("judgments-32")
        self.assertEqual(is_valid, False)

    def test_judgements_file_with_big_number_should_be_valid(self):
        is_valid = is_valid_input_file("judgments-{}.json".format(100000000))
        self.assertEqual(is_valid, True)


if __name__ == '__main__':
    main()
