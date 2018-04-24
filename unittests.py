from unittest.mock import patch
import unittest

from log_model import Log

from peewee import *


def get_input(text):
    return input(text)


# Using an in-memory SQLite db for tests
test_db = SqliteDatabase(':memory:')


class TestWorklogs(unittest.TestCase):
    def setUp(self):
        # Bind model class to test db.
        Log.bind(test_db, bind_refs=False, bind_backrefs=False)

        # Connect to in-memory test database and create Log table
        test_db.connect()
        test_db.create_tables([Log])

        Log.create(
            date='01/01/2000',
            employee_name='Alpha',
            task_name='Task One',
            time_spent=1,
            note='Won')
        Log.create(
            date='01/02/2000',
            employee_name='Beta',
            task_name='Task Two',
            time_spent=2,
            note='Too')

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(Log)

        # Close connection to in-memory test database.
        test_db.close()

    @patch(
        'builtins.input',
        side_effect=[
            '1', '03/03/3000', 'Gamma', 'Task Three', '3', 'Thryee', '', '3'
        ])
    def test_main_menu_add_log(self, input):
        from work_logs_sqlite import main_menu_loop
        main_menu_loop()
        logs = Log.select()
        self.assertEqual(len(logs), 3)
        self.assertEqual(logs[2].date, '03/03/3000')
        self.assertEqual(logs[2].employee_name, 'Gamma')
        self.assertEqual(logs[2].task_name, 'Task Three')
        self.assertEqual(logs[2].time_spent, 3)
        self.assertEqual(logs[2].note, 'Thryee')

    def test_sorting(self):
        from searches import sorting
        self.assertEqual(sorting("01/02/0003"), ('0003', '01', '02'))

    def test_get_distinct_dates(self):
        from searches import get_distinct_dates
        self.assertEqual(get_distinct_dates(), ['01/01/2000', '01/02/2000'])

    def test_get_distinct_names(self):
        from searches import get_distinct_names
        self.assertEqual(get_distinct_names(), ['Alpha', 'Beta'])
        self.assertEqual(get_distinct_names('alph'), ['Alpha'])
        self.assertEqual(get_distinct_names('b'), ['Beta'])

    @patch('builtins.input', return_value='1')
    def test_find_by_date(self, input):
        from searches import find_by_date
        log = find_by_date(['01/01/2000', '01/02/2000'])
        self.assertEqual(log[0].date, '01/01/2000')

    @patch('builtins.input', return_value='2')
    def test_find_by_employee(self, input):
        from searches import find_by_employee
        log = find_by_employee()
        self.assertEqual(log[0].employee_name, 'Beta')

    @patch('builtins.input', return_value='1')
    def test_find_by_name(self, input):
        from searches import find_by_name
        log = find_by_name('be')
        self.assertEqual(log[0].employee_name, 'Beta')

    def test_find_by_string(self):
        from searches import find_by_string
        log = find_by_string('won')
        self.assertEqual(log[0].note, 'Won')

    def test_find_by_date_range(self):
        from searches import find_by_date_range
        log = find_by_date_range("12/31/1999", "01/01/2000")
        self.assertEqual(log[0].date, "01/01/2000")

    def test_find_by_time_spent(self):
        from searches import find_by_time_spent
        log = find_by_time_spent('2')
        self.assertEqual(log[0].time_spent, 2)

    @patch('builtins.input', side_effect=['d', 'y', '', 'r'])
    def test_view_logs_loop_delete_confirm(self, input):
        from work_logs_sqlite import view_logs_loop
        logs = Log.select()
        view_logs_loop(logs)
        assert len(Log.select()) == 1

    @patch('builtins.input', side_effect=['d', 'n', '', 'r'])
    def test_view_logs_loop_delete_disconfirm(self, input):
        from work_logs_sqlite import view_logs_loop
        logs = Log.select()
        view_logs_loop(logs)
        assert len(Log.select()) == 2

    @patch('builtins.input', side_effect=['e', '1', '03/03/3000', '', 'r'])
    def test_view_logs_loop_and_edit_date(self, input):
        from work_logs_sqlite import view_logs_loop
        logs = Log.select()
        view_logs_loop(logs)
        self.assertEqual(Log.select()[0].date, '03/03/3000')

    @patch('builtins.input', side_effect=['e', '2', 'Gamma', '', 'r'])
    def test_view_logs_loop_and_edit_employee_name(self, input):
        from work_logs_sqlite import view_logs_loop
        logs = Log.select()
        view_logs_loop(logs)
        self.assertEqual(Log.select()[0].employee_name, 'Gamma')

    @patch('builtins.input', side_effect=['e', '3', 'Task Three', '', 'r'])
    def test_view_logs_loop_and_edit_task_name(self, input):
        from work_logs_sqlite import view_logs_loop
        logs = Log.select()
        view_logs_loop(logs)
        self.assertEqual(Log.select()[0].task_name, 'Task Three')

    @patch('builtins.input', side_effect=['e', '4', '3', '', 'r'])
    def test_view_logs_loop_and_edit_time_spent(self, input):
        from work_logs_sqlite import view_logs_loop
        logs = Log.select()
        view_logs_loop(logs)
        self.assertEqual(Log.select()[0].time_spent, 3)

    @patch('builtins.input', side_effect=['e', '5', 'Thryee', '', 'r'])
    def test_view_logs_loop_and_edit_note(self, input):
        from work_logs_sqlite import view_logs_loop
        logs = Log.select()
        view_logs_loop(logs)
        self.assertEqual(Log.select()[0].note, 'Thryee')

    @patch(
        'builtins.input',
        side_effect=[
            'e', '6', '03/03/3000', 'Gamma', 'Task Three', '3', 'Thryee', '',
            'r'
        ])
    def test_view_logs_loop_and_edit_all(self, input):
        from work_logs_sqlite import view_logs_loop
        logs = Log.select()
        view_logs_loop(logs)
        logs = Log.select()
        self.assertEqual(logs[0].date, '03/03/3000')
        self.assertEqual(logs[0].employee_name, 'Gamma')
        self.assertEqual(logs[0].task_name, 'Task Three')
        self.assertEqual(logs[0].time_spent, 3)
        self.assertEqual(logs[0].note, 'Thryee')


class TestUserInputFunctions(unittest.TestCase):
    @patch('builtins.input', return_value='1')
    def test_menu(self, input):
        from user_input_functions import menu
        self.assertEqual(menu(['1']), '1')
        self.assertEqual(menu([]), None)

    def test_validate_text(self):
        from user_input_functions import validate_text
        assert validate_text('Test')
        assert not validate_text('   ')
        assert not validate_text('')

    def test_validate_date(self):
        from user_input_functions import validate_date
        assert validate_date('11/11/1111')
        assert not validate_date('13/11/1111')
        assert not validate_date('12/32/1111')
        assert not validate_date('11/11/11')

    def test_validate_time_spent(self):
        from user_input_functions import validate_time_spent
        assert validate_time_spent('1')
        assert not validate_time_spent('One')
        assert not validate_time_spent('1.5')

    @patch('builtins.input', return_value='Test Text')
    def test_get_text(self, input):
        from user_input_functions import get_text
        self.assertEqual(get_text('employee name'), 'Test Text')

    @patch('builtins.input', return_value='11/11/1111')
    def test_get_date(self, input):
        from user_input_functions import get_date
        self.assertEqual(get_date(), '11/11/1111')

    @patch('builtins.input', return_value='1')
    def test_get_time_spent(self, input):
        from user_input_functions import get_time_spent
        self.assertEqual(get_time_spent(), 1)

    @patch('builtins.input', return_value='y')
    def test_positive_confirm_action(self, input):
        from work_logs_sqlite import confirm_action
        assert confirm_action()

    @patch('builtins.input', return_value='n')
    def test_negative_confirm_action(self, input):
        from work_logs_sqlite import confirm_action
        assert not confirm_action()


if __name__ == '__main__':
    unittest.main()

