'''
	current_late_view.py

	Programm, um das Verhältnis
	aktueller und überfälliger Kredite
	je Kreditgeber bei Mintos darzustellen.

	Januar 2020
'''

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate



conn = sqlite3.connect('mintos.db')
c = conn.cursor()
results = c.execute('select "Loan Originator", sum("Initial Loan Amount"), "Loan Status" from mintos_data_2 \
            where "Loan Status" ="Current" or \
            "Loan Status" = "Default" or \
            "Loan Status" = "Grace Period" or \
            "Loan Status" = "Late 1-15" or \
            "Loan Status" = "Late 16-30" or \
            "Loan Status" = "Late 31-60" or \
            "Loan Status" = "Late 60+" \
            and "Currency" = "EUR" \
            group by "Loan Originator", "Loan Status" \
            order by "Loan Originator"')

last_originator = ''
current = 0
overdue = 0
list_current_overdue = []
rating = ''

for counter, line in enumerate(results):
    originator, value, status = line
    if originator != last_originator and counter > 0:
        Perc_Overdue = (overdue/(current+overdue)*100)
        if Perc_Overdue >= 30:
            rating = 'C'
        if Perc_Overdue > 10 and Perc_Overdue < 30:
            rating = 'B'
        if Perc_Overdue <= 10:
            rating = 'A'
        list_current_overdue.append([last_originator, current, overdue, (current/(current+overdue))*100, Perc_Overdue, rating]) 
        current = 0
        overdue = 0
        rating = ''
        last_originator = originator
    else:
        last_originator = originator
    if status == 'Current':
        current += float(value)
    else:
        overdue += float(value)
print(list_current_overdue)
quit()
loan_originator_df = pd.DataFrame.from_records(list_current_overdue, columns=['Originator', 'Current', 'Overdue', 'Perc_Current', 'Perc_Overdue', 'Rating'])
loan_originator_df = loan_originator_df.sort_values(by=['Perc_Current'])
fig = plt.figure()
plt.xlim(0,100)
#plt.style.use('dark_background')
ax1 = fig.add_subplot(111)
ax1.barh(loan_originator_df ['Originator'], loan_originator_df ['Perc_Current'], color = 'g', label = 'Planmäßig')
ax1.barh(loan_originator_df ['Originator'], loan_originator_df ['Perc_Overdue'], color = 'r', left = loan_originator_df ['Perc_Current'], label = 'Überfällig')

#for t3 in ax1.get_yticklabels():
#    t3.set_color('black')
    #plt.margins(0.2)
plt.subplots_adjust(bottom=0.15)
plt.show()
loan_originator_df = loan_originator_df.drop(columns=['Current','Overdue'])
print(tabulate(loan_originator_df , headers='keys', tablefmt='psql', showindex=False))















