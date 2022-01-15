from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6 import QtCore
from PySide6.QtCore import Signal, Slot, QUrl
# import style_rc
import sys
import os
import os.path
import pandas as pd
import numpy as np
import datetime as dt
from Data.DataManagement import ManageTasks

debug = True

##########
# SIDE MENU IMPLEMENTAION
# ADD SETTINGS MENU AND FILE
# IMPLEMENT DARK MODE THEME
##########


class Test(QtCore.QObject):
    '''OBJECT TO CALL FROM JS IN QML. QML PROPERTY SET TO testModel'''

    global tasks

    def __init__(self):
        QtCore.QObject.__init__(self)

    def addNewRepeat(self, repeat):
        repeats_list = list(repeat.split(','))
        repeats_list = list(map(int, repeats_list))
        if any(ele == 1 for ele in repeats_list):
            return repeats_list
        else:
            return False

    def check_repeats(self, dateDT):
        '''Checks for tasks matching day and returns a df of them'''
        col_lst = [
            'Reminder_mon', 'Reminder_tue', 'Reminder_wed', 'Reminder_thu',
            'Reminder_fri', 'Reminder_sat', 'Reminder_sun'
        ]
        repeat_df = pd.read_csv('repeat_df.csv')
        day = dateDT.isoweekday() # Get day of the week as int where Monday is 1
        to_repeat = repeat_df.loc[(repeat_df[list(col_lst)] == day).any(1)] # Return rows where day is in any reminder column
        # to_repeat = to_repeat.drop(col_lst)
        # to_repeat.loc['Date'] = dateDT
        # to_repeat.apply(lambda row: self.addTaskPy(row['Task'], row['Date'], row['Date'], row['Button id'], 0), axis=1)
        # print('!!!!', to_repeat)
        return to_repeat

    def creatButtonPy(self, task, buttonId, date, color, reminder):
        '''GENERATES TASK BUTTONS IN UI'''

        rootObject = engine.rootObjects()[0]
        task = task.split('(')[0]
        task = task.rstrip('\n')
        rootObject.createButton(task, buttonId, date, color, reminder)

    @Slot(str, int, str, str)
    def deleteTaskPy(self, task, buttonId, date, repeat):
        if repeat == '':
            ManageTasks(date, task, buttonId).delete_single_task()
        else:
            ManageTasks(date, task, buttonId).delete_repeat_task()
        self.showTasks(date)

    @Slot(str, str, str)
    def debug(self, text, text1, text2):
        '''Use for printing console.log from JS code'''

        # print(f'Begin Degug:\n{text} {text1} {text2}')
        pass

    def showTasks(self, date):  # SHOW TASKS AS BUTTONS
        rootObject = engine.rootObjects()[0]
        date = dt.datetime.strptime(date, '''%B %d, %Y ''')
        date = date.strftime('''%B %d, %Y ''')
        df_single, df_repeats = ManageTasks(date).gather_tasks()
        df_single.apply(lambda row: self.creatButtonPy(
            row['Task'], row['Button id'], row['Date'], row['Color'], ''
            ), axis=1)
        df_repeats.apply(lambda row: self.creatButtonPy(
            row['Task'], row['Button id'], row['Date'], row['Color'], row['Reminder']
            ), axis=1)
        rootObject.taskBoxReAn()

    @QtCore.Slot(str, str, str, int, str)
    def addTaskPy(self, task, taskDate, date, existingId, repeat=''):  # ADD NEW TASK
        taskDate = dt.datetime.strptime(taskDate, '''%B %d, %Y ''')
        taskDate = taskDate.strftime('''%B %d, %Y ''')
        if repeat == '':
            ManageTasks(taskDate, task, existingId).store_single_task()
        else:
            ManageTasks(taskDate, task, existingId, repeat).store_repeat_task()
       
        self.call()
        self.showTasks(taskDate)

    @QtCore.Slot('QString')
    def call(self):
        '''Destroys buttons in UI'''
        rootObject = engine.rootObjects()[0]
        rootObject.destroyButtons()

    @Slot(int, bool, str)
    def getDatePy(self, day, update, date):  # GET DATE AND FORMAT. ALSO PROVIDES UPDATE CALL FOR WHEN DATE IS UPDATED IN UI
        rootObject = engine.rootObjects()[0]
        plusdays = dt.timedelta(days=day)
        # print(day)
        if day == 0:
            date = dt.datetime.today()
            date = dt.datetime.strftime(date, '''%B %d, %Y ''')
        else:
            date = dt.datetime.strptime(date, '''%B %d, %Y ''') + plusdays
            date = dt.datetime.strftime(date, '''%B %d, %Y ''')

        caldate = dt.datetime.strptime(date, '''%B %d, %Y ''')
        caldateM = int(dt.datetime.strftime(caldate, '''%m '''))
        caldateD = int(dt.datetime.strftime(caldate, '''%d '''))
        caldateY = int(dt.datetime.strftime(caldate, '''%Y '''))
        # caldate = QDate(caldateY, caldateM, caldateD)

        if update is True:
            self.call()
            self.showTasks(date)
            rootObject.taskBoxReAn()

        engine.rootContext().setContextProperty("date", date)


class setup():  # CLASS CONTAINING FUNCTIONS TO BE RAN ON STARTUP OR WHEN SETTINGS ARE UPDATED
    def getSettings(darkMode):  # SETTIGNS/CONFIG FILE AND UI FUNCTIONALITY NOT IMPLEMENTED YET
        if darkMode is True:  # DARKMODE STYLING NOT IMPLEMENTED YET
            import style_rc_dark
        else:
            import style_rc  # DEFAULT STYLE

    def start(x):  # SETS INITIAL PROPERTY TO ENABLE TO CALLS TO PY FROM JS
        engine.rootContext().setContextProperty("testModel", x)
        x.getDatePy(0, True, '')  # SETS DATE TO TODAYS DATE

    def checkDf():
        '''Checks for required df files and if they are not found it creates them'''

        global tasks, taskNum
        if not os.path.exists('df.csv'):
            tasks = pd.DataFrame(columns=['Date', 'Button id', 'Task', 'Color', 'Reminder'])  # SETUP DATAFRAME
            tasks.to_csv('df.csv')
            if debug:
                # print('Debug in class: setup function: start:\nCreated df.csv file as one was not found')
                pass
        if not os.path.exists('repeat_df.csv'):
            tasks = pd.DataFrame(columns=[
                'Date', 'Button id', 'Task', 'Color', 'Reminder_mon', 'Reminder_tue', 'Reminder_wed',
                'Reminder_thu', 'Reminder_fri', 'Reminder_sat', 'Reminder_sun'
            ])  # SETUP DATAFRAME
            tasks.to_csv('repeat_df.csv')
            
        # GLOBAL VARIABLES
        tasks = pd.read_csv('df.csv')  # FILE TO STORE TASKS AND THEIR PROPERTIES
        taskNum = {}

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    directory = os.path.dirname(os.path.abspath(__file__))
    setup.checkDf()
    setup.getSettings(False)
    engine.load(QtCore.QUrl.fromLocalFile(os.path.join(directory, 'ToDoList.qml')))
    # Test = Test()
    # engine.rootContext().setContextProperty("testModel", Test)
    x = Test()
    setup.start(x)
    print('working...')
    if not engine.rootObjects():
        # print('error')
        sys.exit(-1)
    sys.exit(app.exec())
