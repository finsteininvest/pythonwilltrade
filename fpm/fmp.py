'''
	fmp.py

	Sammlung von Funktionen, um
	Daten von financialmodelingprep
	herunterzuladen.

	Erstellt: 1. März 2020 
	https://finsteininvest.pythonanywhere.com/

	Quelle: https://financialmodelingprep.com/
'''

import json
import requests
import pandas as pd

def get_symbols_list(debug=False):
	'''
		Retrieves a dataframe of available 
		symbols, symbol name, latest quote (price)
		and exchange
		from the site.
		Columns are: symbol, name, price, exchange
		Index is set to symbol
	'''
	r = requests.get('https://financialmodelingprep.com/api/v3/company/stock/list')
	symbolsList = json.loads(r.text)


	if debug == True:
		for asset in symbolsList['symbolsList']:
			name = ''
			symbol = ''
			price = 0.00
			try:
				symbol = asset['symbol']
			except:
				pass
			try:
				name = asset['name']
			except:
				pass
			try:
				price = float(asset['price'])
			except:
				pass

			print(f'{symbol} {name} {price}')

	symbols = pd.DataFrame.from_dict(symbolsList['symbolsList'])
	symbols = symbols.set_index('symbol')
	return symbols

def get_historic_values(symbol)
	'''
	'''
	return historic_values
