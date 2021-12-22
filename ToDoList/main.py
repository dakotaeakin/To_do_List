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

debug = True

##########
# ADD DELETE FROM DF, JS FUNCTION CURRENTLY ONLY DELETES FROM UI WHICH CAUSES ERROR WHEN FUNCTION READDED TO DATE
# ADD EDIT TASK FUNCTION
# SIDE MENU IMPLEMENTAION
# ADD SETTINGS MENU AND FILE
# IMPLEMENT DARK MODE THEME
##########


class Test(QtCore.QObject):  # OBJECT TO CALL FROM JS IN QML. QML PROPERTY SET TO testModel
    global tasks

    def __init__(self):
        QtCore.QObject.__init__(self)

    @Slot(int, str)
    def deleteTaskPy(self, buttonId, date):
        tasks = pd.read_csv('df.csv')
        print(tasks)
        tasks.drop(tasks[(tasks['Date'] == date) & (tasks['Button id'] == buttonId)].index, inplace=True)
        self.refreshTasks(date, False)
        tasks.to_csv('df.csv', index=False)


    @Slot(str, str, str)
    def debug(self, text, text1, text2):
        print(f'Begin Degug:\n{text} {text1} {text2}')

    def refreshTasks(self, date, refresh):  # SHOW TASKS AS BUTTONS
        tasks = pd.read_csv('df.csv')
        # print(tasks)
        rootObject = engine.rootObjects()[0]
        date = dt.datetime.strptime(date, '''%B %d, %Y ''')
        date = date.strftime('''%B %d, %Y ''')
        df = tasks.loc[(tasks['Date'] == date)]
        taskList = df['Task'].values.tolist()
        # print('Task is', date)
        if refresh is True:
            i = 0
        for task in taskList:  # LOOP TO CALL JS FUNCTION FOR EACH TASK
            buttonId = df.loc[(df['Task'] == task), 'Button id'].item()
            task = task.split('(')[0]
            task = task.rstrip('\n')
            # print(task)
            rootObject.createButton(task, buttonId, date)
            print('test1', buttonId)
        # else:
        #     for task in taskList:  # LOOP TO CALL JS FUNCTION FOR EACH TASK
        #         task = task.split('(')[0]
        #         task = task.rstrip('\n')
        #         # print(task)
        #         rootObject.createButton(task)

    def showTasks(self, date, refresh, buttonId):  # SHOW TASKS AS BUTTONS
        tasks = pd.read_csv('df.csv')
        print(tasks)
        rootObject = engine.rootObjects()[0]
        date = dt.datetime.strptime(date, '''%B %d, %Y ''')
        date = date.strftime('''%B %d, %Y ''')
        df = tasks.loc[(tasks['Date'] == date)]
        taskList = df['Task'].values.tolist()
        # print('Task is', date)
        if refresh is True:
            i = 0
        for task in taskList:  # LOOP TO CALL JS FUNCTION FOR EACH TASK
            task = task.split('(')[0]
            task = task.rstrip('\n')
            # print(task)
            rootObject.createButton(task, buttonId, date)
        # else:
        #     for task in taskList:  # LOOP TO CALL JS FUNCTION FOR EACH TASK
        #         task = task.split('(')[0]
        #         task = task.rstrip('\n')
        #         # print(task)
        #         rootObject.createButton(task)

    @QtCore.Slot(str, str, str)
    def addTaskPy(self, task, taskDate, date):  # ADD NEW TASK
        # TRY LOOP FAILS IF NUM EXISTS, EDIT TO HANDLE?
        # REPLACE TRY LOOP?
        # global tasks
        global taskNum
        tasks = pd.read_csv('df.csv')
        taskDate = dt.datetime.strptime(taskDate, '''%B %d, %Y ''')
        taskDate = taskDate.strftime('''%B %d, %Y ''')
        #####
        # CHECK IF TASK EXISTS ON DATE
        #####
        try:
            list1 = tasks.loc[(tasks['Date'] == date) & (tasks['Button id'])]
            # if taskDate in taskNum:  # CHANGE PD LOC FOR DATE AND NUM
            num = list1['Button id'].max() + 1
            if np.isnan(num):
                num = 1
            # else:
            #     num = 1
            # np.where(tasks['Date'] == taskDate, num=tasks.loc(tasks['Date'], 'Button id').max(), num=1)
        except Exception as e:
            if debug:
                print(e)
            num = 1
            pass
        # num = list
        buttonId = num
        # taskNum.setdefault(taskDate, []).append(buttonId)

        taskTemp = pd.DataFrame({'Date': [taskDate], 'Button id': [buttonId], 'Task': [f'{task}({taskDate}{taskNum})']})
        taskTemp.to_csv('df.csv', mode='a', header=False)
        self.call()
        self.showTasks(taskDate, True, buttonId)
        # print("date", taskDate)
        # self.showTasks(taskDate)  # Need to add arg for range of dates
        if debug:
            print("test", num)

    @QtCore.Slot('QString')
    def call(self):
        rootObject = engine.rootObjects()[0]
        rootObject.destroyButtons()

    @Slot(int, bool, str)
    def getDatePy(self, day, update, date):  # GET DATE AND FORMAT. ALSO PROVIDES UPDATE CALL FOR WHEN DATE IS UPDATED IN UI
        rootObject = engine.rootObjects()[0]
        plusdays = dt.timedelta(days=day)
        print(day)
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
            self.refreshTasks(date, False)
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
        global tasks, taskNum
        if not os.path.exists('df.csv'):
            tasks = pd.DataFrame(columns=['Date', 'Button id', 'Task', 'Color', 'Reminder'])  # SETUP DATAFRAME
            tasks.to_csv('df.csv')
            if debug:
                print('Debug in class: setup function: start:\nCreated df.csv file as one was not found')
        if debug:
            print('Debug in class: setup function: start:\ndf.csv found')
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
        print('error')
        sys.exit(-1)
    sys.exit(app.exec())
