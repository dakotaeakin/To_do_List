import os
main_dirname = os.path.dirname(__file__)
main_path = os.path.dirname(main_dirname)
os.chdir(os.path.abspath(main_path))

# TODO: Fix working dir

from Data.DataManagement import ManageTasks
# import datetime as dt
# taskDate = 'January 08, 2022 '
# # date = dt.datetime.strptime(taskDate, '''%B %d, %Y ''')

# taskDate = dt.datetime.strptime(taskDate, '''%B %d, %Y ''')
# taskDate = taskDate.strftime('''%B %d, %Y ''')

def test_store_repeat_task():
    combineTasks = ManageTasks('task', taskDate, True, 0, 6)
    combineTasks.store_repeat_task()

def test_store_single_task():
    combineTasks = ManageTasks('task', taskDate, False, 0)
    combineTasks.store_single_task()

def test_gather_tasks():
    combineTasks = ManageTasks('task', taskDate, False, 0)
    result = combineTasks.gather_tasks()
    print(result)

# test_store_repeat_task()

# test_store_single_task()

# test_gather_tasks()

# print(taskDate.isoweekday())

