import datetime

from log_model import Log
from user_input_functions import menu


def sorting(logs):
    '''Defines a sorting key to be used for sorting by date (Y > M > D)'''
    splitup = logs.split('/')
    return splitup[2], splitup[0], splitup[1]


def get_distinct_dates():
    """Returns a list of distinct dates in the db."""
    query = Log.select(Log.date).distinct()
    dates = [log.date for log in query]
    return sorted(dates, key=sorting)


def get_distinct_names(search_term=None):
    """Returns a list of distinct employee names in the db."""
    if search_term:
        query = Log.select(Log.employee_name).distinct().where(
            Log.employee_name.contains(search_term)).order_by(
                Log.employee_name)
    else:
        query = Log.select(Log.employee_name).distinct().order_by(
            Log.employee_name)

    return [log.employee_name for log in query]


def find_by_date(dates):
    """Find by date"""
    chosen_date = menu(dates)
    return Log.select().where(Log.date == chosen_date)


def find_by_employee():
    """Search by a list of employees."""
    chosen_name = menu(get_distinct_names())
    return Log.select().where(Log.employee_name == chosen_name)


def find_by_name(search_term):
    """Find by name."""
    names = get_distinct_names(search_term)
    print("Matches for search: ")
    chosen_name = menu(names)
    return Log.select().where(Log.employee_name == chosen_name)

def find_by_time_spent(search_time):
    """Find by time spent."""
    return Log.select().where(Log.time_spent == int(search_time))


def find_by_date_range(start, end):
    """Searches for work logs by dates within a specified range"""
    start_date = datetime.datetime.strptime(start, '%m/%d/%Y')
    end_date = datetime.datetime.strptime(end, '%m/%d/%Y')

    # Create a timedelta with a value of 0 (for the range's minimum) and
    # calculate a timedelta that represents the maximum value allowed
    # by the search (end_date - start_date)
    range_start = datetime.timedelta(0)
    range_max = end_date - start_date

    # Return a list of logs that have dates falling within the search
    # range.
    logs = Log.select()
    search_results = []
    for log in logs:
        date = end_date - datetime.datetime.strptime(log.date, "%m/%d/%Y")
        if date >= range_start and date <= range_max:
            search_results.append(log)
    return search_results


def find_by_string(search_term):
    """Find by search term."""
    logs = Log.select()
    return (logs.where(Log.task_name.contains(search_term)) or
            logs.where(Log.note.contains(search_term)))

