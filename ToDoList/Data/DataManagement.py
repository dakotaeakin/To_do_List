import os
import os.path
import pandas as pd
import numpy as np
import datetime as dt
import sqlite3
from sqlite3 import Error

class ManageTasks():
    '''Handles backend data storage and parsing'''
    def __init__(self, date, task='', existingId=0, repeat_days=''):
        self.task = task
        self.date = date
        self.repeating = repeat_days
        self.existingId = existingId
        self.repeat_days = repeat_days
        self.dirname = os.path.dirname(__file__)
        self.data_path = os.path.join(self.dirname, 'DataStorage')
        self.repeats_path = (f'{self.data_path}/repeats.csv')
        self.single_path = (f'{self.data_path}/single.csv')
        self.display_path = (f'{self.data_path}/display.csv')
        self.todays_day = dt.datetime.strptime(date, '''%B %d, %Y ''').isoweekday()
        self.check_paths()

    def check_paths(self):
        '''Checks if all database files exists and if any do not creates them'''
        if not os.path.exists(self.repeats_path):
            tasks = pd.DataFrame(columns=['Date', 'Button id', 'Task', 'Color', 'Reminder'])  # SETUP DATAFRAME
            tasks.to_csv(self.repeats_path)
        if not os.path.exists(self.single_path):
            tasks = pd.DataFrame(columns=['Date', 'Button id', 'Task', 'Color', 'Reminder'])  # SETUP DATAFRAME
            tasks.to_csv(self.single_path)
        if not os.path.exists(self.display_path):
            tasks = pd.DataFrame(columns=['Date', 'Button id', 'Task', 'Color', 'Reminder'])  # SETUP DATAFRAME
            tasks.to_csv(self.display_path)

    def store_repeat_task(self):
        '''Saves tasks that do repeat to file'''
        tasks = pd.read_csv(self.repeats_path)
        taskDate = dt.datetime.strptime(self.date, '''%B %d, %Y ''')
        taskDate = taskDate.strftime('''%B %d, %Y ''')
        
        buttonId = self.check_if_task(tasks)
        
        taskTemp = pd.DataFrame({
            'Date': [taskDate], 'Button id': [buttonId], 'Task': [f'{self.task}({taskDate})'],
            'Color': [''], 'Reminder' : [self.repeat_days]
            })
        taskTemp.to_csv(self.repeats_path, mode='a', header=False)

    def store_single_task(self):
        '''Saves tasks that do not repeat to file'''
        tasks = pd.read_csv(self.single_path)
        taskDate = dt.datetime.strptime(self.date, '''%B %d, %Y ''')
        taskDate = taskDate.strftime('''%B %d, %Y ''')
        
        buttonId = self.check_if_task(tasks)
        
        taskTemp = pd.DataFrame({'Date': [taskDate], 'Button id': [buttonId], 'Task': [f'{self.task}({taskDate})']})
        taskTemp.to_csv(self.single_path, mode='a', header=False)

    def delete_repeat_task(self):
        '''Deletes tasks that were repeating from file'''
        tasks = pd.read_csv(self.repeats_path)
        print(self.existingId)    
        tasks.drop(tasks[(tasks['Button id'] == self.existingId)].index, inplace=True)
        tasks.to_csv(self.repeats_path, index=False)

    def delete_single_task(self):
        '''Deletes tasks that were not repeating from file'''
        tasks = pd.read_csv(self.single_path)      
        tasks.drop(tasks[(tasks['Date'] == self.date) & (tasks['Button id'] == self.existingId)].index, inplace=True)
        tasks.to_csv(self.single_path, index=False)

    def gather_tasks(self):
        '''Returns tuple (single_df, repeats_df) of both dataframes sorted by date and isoweekday.'''
        tasks_single = pd.read_csv(self.single_path)
        tasks_repeats = pd.read_csv(self.repeats_path)
        taskDate = dt.datetime.strptime(self.date, '''%B %d, %Y ''')
        taskDate = taskDate.strftime('''%B %d, %Y ''')
        single_df = tasks_single.loc[(tasks_single['Date'] == taskDate)]

        repeats_df = tasks_repeats.loc[tasks_repeats['Reminder'].str.contains(str(self.todays_day))]
        return single_df, repeats_df

    def push_tasks(self):
        pass

    def check_if_task(self, tasks):
        '''Checks if a task already exists on the given date and returns a unique buttonId'''
        if self.existingId != 0:
            buttonId = self.existingId
        else:
            try:
                list1 = tasks.loc[(tasks['Date'] == self.date)]
                print(list1['Button id'])
                num = list1['Button id'].max() + 1
                if np.isnan(num):
                    num = 1
            except Exception as e:
                num = 1
                pass
            buttonId = num
        return buttonId

    def clean_up(self):
        pass

