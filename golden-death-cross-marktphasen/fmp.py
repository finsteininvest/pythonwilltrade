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
		Columns are: 
			symbol, name, price, exchange
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

def get_historic_values(symbol, debug = False):
	'''
		Retrieves a dataframe for a giver symbol.
		For indexes see get_historic_values_index

		Index is set to date.
	'''
	r = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}')
	historic_list = json.loads(r.text)
	if debug == True:
		for entry in historic_list['historical']:
			print(entry['date'])

	historic_values = pd.DataFrame.from_dict(historic_list['historical'])
	historic_values = historic_values.set_index('date')
	return historic_values


def get_historic_values_index(symbol, debug = False):
	'''
		Retrieves a dataframe for a giver index.
		For strocks see get_historic_values

		Index is set to date.
	'''
	r = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/index/{symbol}')
	historic_list = json.loads(r.text)
	if debug == True:
		for entry in historic_list['historical']:
			print(entry['date'])

	historic_values = pd.DataFrame.from_dict(historic_list['historical'])
	historic_values = historic_values.sort_values(by=['date'], ascending=True)
	historic_values = historic_values.set_index('date')
	return historic_values