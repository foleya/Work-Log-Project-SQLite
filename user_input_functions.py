from collections import OrderedDict
import datetime


def menu(option_list):
    '''Displays a menu and returns user's choice'''
    if option_list:
        # Create a list of as many bullets as there are options.
        bullet_list = []
        for num in range(1, len(option_list) + 1):
            bullet_list.append(str(num))

        # Create an ordered dictionary of bullets and options, then print it.
        option_dict = OrderedDict(zip(bullet_list, option_list))
        for number, option in option_dict.items():
            print("{}: {}".format(number, option))

        # Prompt user to enter a number that corresponds with their desired
        # option. Looping until the user enters a valid number choice.
        while True:
            nav = input("Choose an option (1-{}): ".format(len(option_list)))
            try:
                option_dict[nav]
            except KeyError:
                print("\nSorry, '{}' is not a valid option. "
                      "Please choose a number 1-{}."
                      "\n".format(nav, len(option_dict)))
            else:
                break
        return option_dict[nav]

    else:
        return None


def validate_text(input):
    """Checks whether a string is empty (i.e. user input is empty)"""
    if len(input.replace(" ", "")) == 0:
        print("\n---Sorry! This field cannot be empty. Try again!---\n")
        return False
    else:
        return True


def validate_date(input):
    """Checks whether a string has the proper date format (MM/DD/YYYY)"""
    try:
        datetime.datetime.strptime(input, '%m/%d/%Y')
    except ValueError:
        print("\n"
              "--- Sorry, '{}' is not a valid date format. "
              "Please use MM/DD/YYYY. ---"
              "\n".format(input))
        return False
    else:
        return True


def validate_time_spent(input):
    """Checks whether a string can be converted into an integer"""
    try:
        int(input)
    except ValueError:
        print("\n--- Sorry, '{}' is not a whole number. "
              "Please enter a whole number. ---\n".format(input))
        return False
    else:
        return True


def get_text(field_type='text', optional=False):
    if optional is False:
        valid_input = False
        while valid_input is False:
            name = input("Enter {0}: ".format(field_type))
            valid_input = validate_text(name)
    else:
        name = input("Enter {0}: ".format(field_type))
    return name


def get_date():
    '''
    Prompts the user to enter a date with format MM/DD/YYYY
    
    This prompts the user to enter a date, looping until the date entered
    has the proper format: MM/DD/YYYY.
    
    Arguments: None
    Returns: Datetime Object (with format MM/DD/YYYY)
    '''
    valid_input = False
    while valid_input is False:
        date = input('Enter date (MM/DD/YYYY): ')
        valid_input = validate_date(date)
    return date


def get_time_spent():
    '''Prompts user to enter time_spent in rounded minutes'''
    valid_input = False
    while valid_input is False:
        time_spent = input('Enter time spent working in minutes (rounded): ')
        valid_input = validate_time_spent(time_spent)
    return int(time_spent)

