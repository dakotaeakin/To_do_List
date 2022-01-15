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
        '''Deprectaed in ManageData branch, will be removed in future versions'''

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
            from qml.styles import style_rc  # DEFAULT STYLE

    def start(x):  # SETS INITIAL PROPERTY TO ENABLE TO CALLS TO PY FROM JS
        engine.rootContext().setContextProperty("testModel", x)
        x.getDatePy(0, True, '')  # SETS DATE TO TODAYS DATE
            
        # GLOBAL VARIABLES
        taskNum = {}

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    directory = os.path.dirname(os.path.abspath(__file__))
    main_dirname = os.path.dirname(__file__)
    qml_path = os.path.join(main_dirname, 'qml')
    main_qml_script_path = (f'{qml_path}/ToDoList.qml')
    setup.getSettings(False)
    engine.load(QtCore.QUrl.fromLocalFile(main_qml_script_path))
    x = Test()
    setup.start(x)
    print('working...')
    if not engine.rootObjects():
        # print('error')
        sys.exit(-1)
    sys.exit(app.exec())
