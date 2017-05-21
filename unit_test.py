import unittest

from python_file_reader import is_not_valid_date, split_line, is_row_valid, insert_valid_rows, \
    is_user_entry_valid


class TestIsNotValidDate(unittest.TestCase):
    def test_not_valid_date1(self):
        self.assertTrue(is_not_valid_date(r"2016-06-100-17:53:22"))

    def test_not_valid_date2(self):
        self.assertTrue(is_not_valid_date(r"1111-06-10-17:69:22"))

    def test_valid_date3(self):
        expected = False
        actual = is_not_valid_date(r"2016-06-10-17:53:22")
        self.assertEqual(expected, actual)


class TestSplitLine(unittest.TestCase):
    def test_split1(self):
        expected = ['8', '2016-06-10-17:53:22', 'Str1', 'Value', 'Str3']
        actual = split_line(r'8 2016-06-10-17:53:22 Str1 Value Str3')
        self.assertEqual(expected, actual)

    def test_split2(self):
        expected = ['10', '2016-06-10-17:53:22', '"Also invalid"', 'Str2']
        actual = split_line(r'10 2016-06-10-17:53:22 "Also invalid" Str2')
        self.assertEqual(expected, actual)

    def test_split3(self):
        expected = [
            '7',
            '2016-06-10-17:53:22',
            '"A quoted string we don’t care about"',
            '"The string we do care about."',
            '"Another string we don’t are about with escaped\\" \\" quotes. "']
        actual = split_line(
            r'7 2016-06-10-17:53:22 "A quoted string we don’t care about" "The string we do care about." "Another '
            r'string we don’t are about with escaped\" \" quotes. "')
        self.assertEqual(expected, actual)


class TestRowValidity(unittest.TestCase):
    def test_check_row_validity1(self):
        row = ['8', '2016-06-10-17:53:22', 'Str1', 'Value', 'Str3']
        expected = True
        actual = is_row_valid(row)
        self.assertEqual(expected, actual)

    def test_check_row_validity2(self):
        row = [
            '-1',
            '2016-06-10-17:53:22',
            '"This line is invalid"',
            'Str2',
            'Str3']
        expected = False
        actual = is_row_valid(row)
        self.assertEqual(expected, actual)

    def test_check_row_validity3(self):
        row = [
            '7',
            '2016-06-10-17:53:22',
            '"A quoted string we don’t care about"',
            '"The string we do care about."',
            '"Another string we don’t are about with escaped\\" \\" quotes. "']
        expected = True
        actual = is_row_valid(row)
        self.assertEqual(expected, actual)

    def test_check_row_validity4(self):
        row = ['10', '1111-06-10-17:69:22', '"Also invalid"', 'Str2', 'Str3']
        expected = False
        actual = is_row_valid(row)
        self.assertEqual(expected, actual)

    def test_check_row_validity5(self):
        row = [
            '10',
            '2016-06-10',
            '17:53:22',
            '"Also invalid"',
            'Str2',
            'Str3']
        expected = False
        actual = is_row_valid(row)
        self.assertEqual(expected, actual)

    def test_check_row_validity6(self):
        row = [""]
        expected = False
        actual = is_row_valid(row)
        self.assertEqual(expected, actual)

    def test_check_row_validity7(self):
        row = []
        expected = False
        actual = is_row_valid(row)
        self.assertEqual(expected, actual)


class TestUserEntry(unittest.TestCase):
    row1 = ['8', '2016-06-10-17:53:22', 'Str1', 'Value', 'Str3']
    row2 = ['9', '2016-06-10-17:53:22', 'Str1', 'Value2', 'Str3']
    insert_valid_rows(row1)
    insert_valid_rows(row2)

    def test_check_valid_user_entry1(self):
        expected = True
        actual = is_user_entry_valid("8")
        self.assertEqual(expected, actual)

    def test_check_valid_user_entry2(self):
        expected = False
        actual = is_user_entry_valid("fghfhgfhg")
        self.assertEqual(expected, actual)

    def test_check_valid_user_entry3(self):
        expected = False
        actual = is_user_entry_valid("")
        self.assertEqual(expected, actual)

    def test_check_valid_user_entry4(self):
        expected = True
        actual = is_user_entry_valid("9")
        self.assertEqual(expected, actual)

    def test_check_valid_user_entry5(self):
        expected = False
        actual = is_user_entry_valid("6")
        self.assertEqual(expected, actual)

    def test_check_valid_user_entry6(self):
        expected = False
        actual = is_user_entry_valid(",,,,,")
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
