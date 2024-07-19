import json
import numpy as np
import pandas as pd
import yfinance as yf

                    ##############################################
                    ############### NumPy Library    #############
                    ##############################################
jeff_salary = [2700, 3000, 3000]
nick_salary = [2600, 2800, 2800]
tom_salary = [2300, 2500, 2500]

jeff_bonus = [500, 400, 400]
nick_bonus = [600, 300, 400]
tom_bonus = [200, 500, 400]

base_salary = np.array([jeff_salary, nick_salary, tom_salary])
bonus = np.array([jeff_bonus, nick_bonus, tom_bonus])
"""Sum each employees salary and bonus"""
salary_bonus = base_salary + bonus
"""Find max for each employee by rows(1) or cols(0)"""
np.amax(salary_bonus, axis=0)

maya_salary = [2200, 2400, 2400]
john_salary = [2500, 2700, 2700]

base_salary1 = np.array([maya_salary, john_salary])

base_salary_all = np.concatenate((base_salary, base_salary1), axis=0)
print(base_salary_all)


                    ##############################################
                    ###############        Pandas    #############
                    ##############################################

names = ['Jeff Russell', 'Jane Boorman', 'Tom Heints']
emails = ['jeff.russell', 'jane.boorman', 'tom.heints']
emps_names = pd.Series(names)
"""Give the names custom indexes, and get values by given indexes (emps_names_indexes[9001])"""
emps_names_index = pd.Series(names, index=[9001, 9002, 9003])
"""Concat names and emails by the same indexes"""
emps_names_index.name = 'names'
emps_emails_index = pd.Series(emails, index=[9001, 9002, 9003], name='emails')
df = pd.concat([emps_names_index, emps_emails_index], axis=1)
"""Give names to columns and set indexes, and append a new emp to the list"""
data = [['9001','Jeff Russell', 'sales'],
        ['9002','Jane Boorman', 'sales'],
        ['9003','Tom Heints', 'sales']
    ]
new_emps = pd.Series({'Name':'John Hardy', 'Job':'sales'}, name=9004)
emps = pd.DataFrame(data, columns = ['Empno', 'Name', 'Job'])
column_types = {'Empno':int, 'Name':str, 'Job':str}
emps = emps.astype(column_types)
column_types = {'Empno': int, 'Name': str, 'Job': str}
emps = emps.astype(column_types)
emps = emps.set_index('Empno')
emps = emps._append(new_emps)

                    ##############################################
                    ###############    Yahoo Finance #############
                    ##############################################
tkr = yf.Ticker('BTC-USD')
hist = tkr.history(period="1mo")
hist = hist.drop("Dividends", axis=1)
hist = hist.drop("Stock Splits", axis=1)
hist = hist.reset_index()
hist = hist.set_index("Date")
print(hist)