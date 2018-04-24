#!/usr/bin/env python3
import os

from log_model import initialize, Log
from searches import (find_by_date, find_by_employee, find_by_name,
                      find_by_date_range, find_by_string, find_by_time_spent,
                      get_distinct_dates)
from user_input_functions import menu, get_date, get_text, get_time_spent


def clear():
    """Clears the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def confirm_action():
    confirm = input("Confirm this change (y/N)?").lower().strip()
    if confirm == 'y':
        return True
    else:
        return False


def display_log(log):
    print("Date: " + log.date)
    print("Employee: " + log.employee_name)
    print("Task Name: " + log.task_name)
    print("Time Spent: " + str(log.time_spent) + " minute(s)")
    print("Optional Note: " + log.note)


def main_menu_loop():
    main_menu = ['Add Log', 'Search Logs', 'Exit Program']
    while True:
        clear()
        nav = menu(main_menu)

        if nav == 'Add Log':
            date = get_date()
            employee_name = get_text('employee name', optional=False)
            task_name = get_text('task name', optional=False)
            time_spent = get_time_spent()
            note = get_text('note', optional=True)

            Log.create(
                date=date,
                employee_name=employee_name,
                task_name=task_name,
                time_spent=time_spent,
                note=note)
            
            input("\nLog Created! Press any key to continue.")

        if nav == 'Search Logs':
            search_loop()

        if nav == 'Exit Program':
            break


def search_loop():
    """Search menu."""
    search_menu = [
        'Select Date', 'Select Employee Name', 'Search for Employee Name',
        'Search for Word or Phrase', 'Search Date Range',
        'Search by Time Spent', 'Return to Main Menu'
    ]
    while True:
        clear()
        nav = menu(search_menu)

        if nav == 'Select Date':
            search_results = find_by_date(get_distinct_dates())

        if nav == 'Select Employee Name':
            search_results = find_by_employee()

        if nav == 'Search for Employee Name':
            name = input("Enter a name to search for: ")
            search_results = find_by_name(name)

        if nav == 'Search for Word or Phrase':
            term = input("Enter a word or phrase to search for: ")
            search_results = find_by_string(term)

        if nav == 'Search Date Range':
            print("Enter the start date for your search: ")
            start_date = get_date()
            print("Enter the end date for your search: ")
            end_date = get_date()
            search_results = find_by_date_range(start_date, end_date)

        if nav == 'Search by Time Spent':
            search_time = get_time_spent()
            search_results = find_by_time_spent(search_time)

        if nav == 'Return to Main Menu':
            break

        view_logs_loop(search_results)


def view_logs_loop(search_results):
    """View previous entries."""
    if len(search_results) == 0:
        clear()
        input("\n---Sorry, no search results were found. "
              "Press any key to continue.---\n")
    else:
        index = 0
        while True:
            clear()
            print("Displaying result "
                  "{} of {}".format(index + 1, len(search_results)))
            display_log(search_results[index])

            # Display navigation options for the search result detail
            # view.
            nav = input("[N]ext, [P]revious, [E]dit, [D]elete, "
                        "[R]eturn to Search Menu: ").lower()

            # Page to next result (if any)
            if nav == 'n' and index != len(search_results) - 1:
                index += 1

            # Page to previous result (if any)
            if nav == 'p' and index != 0:
                index -= 1

            # Enter edit log dialogue.
            if nav == 'e':
                edit_log(search_results[index])
                break

            # Enter delete log dialogue.
            if nav == 'd':
                print("You have chosen to delete this log.")
                if confirm_action():
                    input("Log Deleted! Press any key to continue.")
                    search_results[index].delete_instance()
                else:
                    input("Log Preserved! Press any key to continue.")
                break

            # Break search result detail view loop if [R]eturn is
            # selected.
            if nav == 'r':
                break

            # Keep loop going if navigation input is invalid.
            else:
                clear()
                continue


def edit_log(log):
    edit_options = [
        'Date', 'Employee Name', 'Task Name', 'Time Spent', 'Note',
        'All Fields', 'No Fields'
    ]
    field = menu(edit_options)

    if field == 'All Fields' or field == 'Date':
        log.date = get_date()

    if field == 'All Fields' or field == 'Employee Name':
        log.employee_name = get_text('employee name', optional=False)

    if field == 'All Fields' or field == 'Task Name':
        log.task_name = get_text('task name', optional=False)

    if field == 'All Fields' or field == 'Time Spent':
        log.time_spent = get_time_spent()

    if field == 'All Fields' or field == 'Note':
        log.note = get_text('note', optional=True)

    log.save()
    input("Log editted! Press any key to continue.")


if __name__ == '__main__':
    initialize()
    main_menu_loop()

