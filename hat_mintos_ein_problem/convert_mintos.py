'''
	convert_mintos.py

	Programm, um die Loan Book Excel Dateien 
	von Mintos in CSV umzuwandeln.
	Anschliessend wird die CSV Datei
	in eine SQLite3 Datenbank importiert.
	Falls die Datenbank oder die Tabelle nicht
	existiert, wird diese angelegt.

	Januar 2020
'''

import pandas as pd
import os

cmd = f'sqlite3 mintos.db -cmd ".read create_table.sql" ".quit"'
rc = os.system(cmd)
print(rc)

zaehler = 0

files = os.listdir()
for file in files:
	if 'xlsx' in file:
		print(f'Start {file}')
		data = pd.read_excel(file, index_col = 0)
		file_name_csv = file.replace('xlsx', 'csv')
		data.to_csv(file_name_csv, header = False, decimal = ',', sep = ';')

		cmd = f'sqlite3 mintos.db -cmd ".mode csv" ".separator \';\'" ".import {file_name_csv} mintos_data"'
		rc = os.system(cmd)
		print(rc)
		rc = os.system(f'rm {file_name_csv}')
		print(rc)
		zaehler = zaehler + 1
		print(f'{zaehler} Dateien von {len(files)} erledigt.')