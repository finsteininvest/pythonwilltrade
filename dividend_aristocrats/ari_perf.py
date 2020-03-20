'''
	ari_perf.py

	Programm, um die Performance von Aktien
	zu prüfen.
	Nutzt Daten von https://financialmodelingprep.com
	und die Liste der Dividenden Aristocraten von
	https://www.suredividend.com/dividend-aristocrats-list/

	März 2020

	https://finsteininvest.pythonanywhere.com/
	https://github.com/finsteininvest/pythonwilltrade
'''

import csv
import requests
import pandas as pd
import json

def check_performance(symbol, name):
	start = '2020-01-01'
	end = '2020-03-19'
	r = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={start}&to={end}')
	historic_list = json.loads(r.text)
	perf = 0
	try:
		historic_values = pd.DataFrame.from_dict(historic_list['historical'])
		historic_values = historic_values.sort_values(by=['date'])
		historic_values = historic_values.set_index('date')

		start_val = historic_values['close'].iloc[0]
		end_val = historic_values['close'].iloc[-1]
		delta = end_val - start_val
		perf = (delta/start_val)*100
		print(f'{name:40} {perf:>.2f}%')
	except:
		pass
	return(perf)

with open('div_aristocrats.csv', 'r') as csvfile:
	 csvreader = csv.reader(csvfile, delimiter=';')
	 perf_list = []
	 for row in csvreader:
	 	perf = check_performance(row[0], row[1])
	 	perf_list.append([row[1], perf])

	 print(perf_list)
	 df = pd.DataFrame.from_records(perf_list, columns=['name', 'perf%'])
	 df = df.sort_values(by=['perf%'], ascending = False)
	 print(df.to_string())


