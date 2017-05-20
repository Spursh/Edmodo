import datetime
import sys
import re
from collections import defaultdict
from Tools.scripts.treesync import raw_input
from dateutil.parser import parse

dictionary = defaultdict(list)

def split_line(current_line):
    """Splits the row into fields with respect to whitespace and double quotes.
    It will not split on whitespace if they are present inside double quotes.
    Example:
        Row before split: 10 2016-06-10 17:53:22 "Also invalid" Str2 Str3
        Row after split:  ['10', '2016-06-10', '17:53:22', '"Also invalid"', 'Str2', 'Str3']
    :param current_line: The row that will split according to the regex defined
    :return: List of fields in a given row after split
    """
    fields = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', current_line)
    return fields


def is_not_valid_date(timestamp):
    """Converts String field to datetime type.
    Checks the datetime validity in 'try ... except' block.
    Invalid datetime value will give 'ValueError' exception.
    :param timestamp: String that is to be checked for valid datetime type.
    :return: False if valid datetime else True
    """
    try:
        isinstance(parse(timestamp), datetime.datetime)
        return False
    except ValueError:
        return True


def is_row_valid(fields_in_row):
    """Checks for the validity of the current row
    :param fields_in_row: List containing all the fields of a row in the file after it has been split by the function 'split_line()'
    :return: "invalid" if successful else "valid"
    """
    if fields_in_row is None or fields_in_row.__len__() is not 5 or int(
            fields_in_row[0]) <= 0 or is_not_valid_date(fields_in_row[1]):
        """ If either of the below conditions are true, the row is invalid
         1. If the row is empty
         2. If the number of fields in a row is not equal to 5
         3. If ID is not a positive number
         4. If date-time field is not of type <class 'datetime.datetime'>
        """
        return False
    else:
        return True


def insert_valid_rows(fields):
    """Insert valid rows into dictionary for fast lookup
    :param fields: List containing fields that is to be stored in dictionary
    :return:
    """
    value_id=0
    value_pos=3
    key = fields[value_id]
    value = fields[value_pos]
    dictionary[key].append(value)
    return dictionary


def requested_output(user_input):  # how to test this function
    """Looks up into the dictionary for the user entered IDs separated with ','.
    :param user_input: Id entered by the user whose value is to be looked up in dictionary and displayed to user
    """
    ids = user_input.split(',')
    ids[-1] = ids[-1].strip("\n")
    for i in ids:
        i = i.strip()
        check_valid_user_entry(i, dictionary) # dictionary add for unit test
        j = list(dictionary[i])
        for k in j:
            print(i + " " + k)


def check_valid_user_entry(i, dictionary):  # dictionary add kiye for unit test
    """Checks whether User's entered data is valid or not
    :param i: User entered value
    :param dictionary: 
    :return: User's entered value if successful else "Invalid Id"
    """
    if i.isdigit() and i in dictionary:
        return True
    else:
        print("Invalid")
        return False


def information_retrieval_on_ids():
    """Reads the user input from the console and passes the value to the function 'requested_output' """
    user_input = raw_input("Enter ids")
    print("Requested Ids", user_input)
    requested_output(user_input)


def get_entry(row_data): #what name should be given to this function
    """Reads through the entire file.
    Counts the total number of invalid rows in a file
    :param row_data: List of lines in a file
    """
    number_of_invalid_rows = 0
    for line in row_data:
        fields_in_a_row = split_line(line)
        row_validity = is_row_valid(fields_in_a_row)
        if row_validity is False:
            number_of_invalid_rows += 1
        else:
            insert_valid_rows(fields_in_a_row)
    print("Number of errors in the given file", number_of_invalid_rows)


def get_user_input_to_continue():
    """Provides an option to the user whether he wants to continue running the application or stop"""
    while True:
        do_you_want_to_continue = raw_input(
            "Do you want to continue \n Yes or No ")
        do_you_want_to_continue = do_you_want_to_continue.strip("\n")
        if do_you_want_to_continue.lower() == "yes":
            information_retrieval_on_ids()
            continue
        elif do_you_want_to_continue.lower() == "no":
            break
        else:
            print("Invalid entry. Please enter a valid option ")
            continue


if __name__ == "__main__":
    file_name = sys.argv[1]
    try:
        with open(file_name) as file:
            data = file.readlines()
            get_entry(data)  #give a proper name
            information_retrieval_on_ids()
            get_user_input_to_continue()
    except IOError:
        print("Could not open file! Please enter valid file")