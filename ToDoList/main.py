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
# !DONE! ADD DELETE FROM DF, JS FUNCTION CURRENTLY ONLY DELETES FROM UI WHICH CAUSES ERROR WHEN FUNCTION READDED TO DATE
# !DONE! ADD EDIT TASK FUNCTION
# SIDE MENU IMPLEMENTAION
# ADD SETTINGS MENU AND FILE
# IMPLEMENT DARK MODE THEME
##########


class Test(QtCore.QObject):
    '''OBJECT TO CALL FROM JS IN QML. QML PROPERTY SET TO testModel'''

    global tasks

    def __init__(self):
        QtCore.QObject.__init__(self)

    def check_repeats(self, dateDT):
        '''Checks for tasks matching day and returns a df of them'''

        repeat_df = pd.read_csv('repeat_df.csv')
        day = dateDT.isoweekday() # Get day of the week as int where Monday is 1
        to_repeat = repeat_df.loc[(repeat_df['Reminder'] == day)]
        return to_repeat


    def creatButtonPy(self, task, buttonId, date):
        '''GENERATES TASK BUTTONS IN UI'''

        rootObject = engine.rootObjects()[0]
        task = task.split('(')[0]
        task = task.rstrip('\n')
        rootObject.createButton(task, buttonId, date)

    @Slot(int, str)
    def deleteTaskPy(self, buttonId, date):
        tasks = pd.read_csv('df.csv')
        tasks.drop(tasks[(tasks['Date'] == date) & (tasks['Button id'] == buttonId)].index, inplace=True)
        tasks.to_csv('df.csv', index=False)
        self.showTasks(date)

    @Slot(str, str, str)
    def debug(self, text, text1, text2):
        '''Use for printing console.log from JS code'''

        print(f'Begin Degug:\n{text} {text1} {text2}')

    def showTasks(self, date):  # SHOW TASKS AS BUTTONS
        rootObject = engine.rootObjects()[0]
        tasks = pd.read_csv('df.csv')
        date = dt.datetime.strptime(date, '''%B %d, %Y ''')
        dateDT = date
        date = date.strftime('''%B %d, %Y ''')
        df = tasks.loc[(tasks['Date'] == date)]
        df = df.append(self.check_repeats(dateDT)) 
        print(df)
        df.apply(lambda row: self.creatButtonPy(row['Task'], row['Button id'], row['Date']), axis=1)
        rootObject.taskBoxReAn()

    @QtCore.Slot(str, str, str, int)
    def addTaskPy(self, task, taskDate, date, existingId):  # ADD NEW TASK
        # REPLACE TRY LOOP?
        # global tasks
        global taskNum
        tasks = pd.read_csv('df.csv')
        taskDate = dt.datetime.strptime(taskDate, '''%B %d, %Y ''')
        taskDate = taskDate.strftime('''%B %d, %Y ''')
        #####
        # CHECK IF TASK EXISTS ON DATE
        #####
        if existingId != 0:
            buttonId = existingId
        else:
            try:
                list1 = tasks.loc[(tasks['Date'] == date)]
                print(list1['Button id'])
                num = list1['Button id'].max() + 1
                if np.isnan(num):
                    num = 1
            except Exception as e:
                if debug:
                    print(e)
                num = 1
                pass
            buttonId = num

        taskTemp = pd.DataFrame({'Date': [taskDate], 'Button id': [buttonId], 'Task': [f'{task}({taskDate}{taskNum})']})
        taskTemp.to_csv('df.csv', mode='a', header=False)
        self.call()
        self.showTasks(taskDate)

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
                print('Debug in class: setup function: start:\nCreated df.csv file as one was not found')
        
        if not os.path.exists('repeat_df.csv'):
            tasks = pd.DataFrame(columns=['Date', 'Button id', 'Task', 'Color', 'Reminder'])  # SETUP DATAFRAME
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
        print('error')
        sys.exit(-1)
    sys.exit(app.exec())
