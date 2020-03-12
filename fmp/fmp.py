'''
	fmp.py

	Sammlung von Funktionen, um
	Daten von financialmodelingprep
	herunterzuladen.

	Erstellt: 1. März 2020
	Erweitert: 10. März 2020

	https://finsteininvest.pythonanywhere.com/
	https://github.com/finsteininvest/pythonwilltrade/tree/master/fmp
	
	Nutzt: https://financialmodelingprep.com/
'''

import json
import requests
import pandas as pd
import scipy
from scipy import stats

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

def get_historic_values(symbol, type, debug = False):
	'''
		Retrieves a dataframe for historic values
		for a given symbol and type.

		Index is set to date.

		Possible type(s)
		- empty = stock
		- index/
		- crypto/

	'''
	r = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{type}{symbol}')
	historic_list = json.loads(r.text)
	if debug == True:
		for entry in historic_list['historical']:
			print(entry['date'])

	historic_values = pd.DataFrame.from_dict(historic_list['historical'])
	historic_values = historic_values.sort_values(by=['date'])
	historic_values = historic_values.set_index('date')

	return historic_values

def get_historic_eps(symbol, debug=False):
	'''
		Retrieves a dataframe for eps
		for a given symbol.

		Index is set to date
	'''
	r = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{symbol}')
	historic_eps_list = json.loads(r.text)
	if debug == True:
		for entry in historic_eps_list['financials']:
			print(entry['date'])
	historic_eps_values = pd.DataFrame.from_dict(historic_eps_list['financials'])
	historic_eps_values = historic_eps_values.sort_values(by=['date'])
	historic_eps_values = historic_eps_values[['date', 'EPS']]
	historic_eps_values = historic_eps_values.set_index('date')

	return historic_eps_values

def get_historic_roe(symbol, debug = False):
	'''
		Retrieves a dataframe for roe
		for a given symbol.

		Index is set to date
	'''
	r = requests.get(f'https://financialmodelingprep.com/api/v3/company-key-metrics/{symbol}')
	historic_roe_value_list = json.loads(r.text)
	if debug == True:
		for entry in historic_roe_value_list['metrics']:
			print(entry['date'])
	historic_roe_values = pd.DataFrame.from_dict(historic_roe_value_list['metrics'])
	historic_roe_values = historic_roe_values.sort_values(by=['date'])
	historic_roe_values = historic_roe_values[['date', 'ROE']]
	historic_roe_values = historic_roe_values.set_index('date')

	return historic_roe_values

def get_historic_dividend(symbol, debug = False):
	'''
		Retrieves a dataframe for dividens
		for a given symbol.

		Index is set to date
	'''
	r = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{symbol}')
	historic_dividend_list = json.loads(r.text)
	if debug == True:
		for entry in historic_dividend_list['historical']:
			print(entry['date'])
	historic_dividend_values = pd.DataFrame.from_dict(historic_dividend_list['historical'])
	historic_dividend_values = historic_dividend_values.sort_values(by=['date'])
	historic_dividend_values = historic_dividend_values[['date', 'adjDividend']]
	historic_dividend_values['date'] = pd.to_datetime(historic_dividend_values['date'])
	historic_dividend_values = historic_dividend_values.set_index('date')
	historic_dividend_values = historic_dividend_values.resample('Y').sum()
	return historic_dividend_values

def get_book_value_per_share(symbol, debug = False):
	'''
		Retrieves a dataframe for book value per share
		for a given symbol.

		Index is set to date
	'''
	r = requests.get(f'https://financialmodelingprep.com/api/v3/company-key-metrics/{symbol}')
	historic_book_value_list = json.loads(r.text)
	if debug == True:
		for entry in historic_book_value_list['metrics']:
			print(entry['date'])
	historic_book_values = pd.DataFrame.from_dict(historic_book_value_list['metrics'])
	historic_book_values = historic_book_values.sort_values(by=['date'])
	historic_book_values = historic_book_values[['date', 'Book Value per Share']]
	historic_book_values = historic_book_values.set_index('date')

	return historic_book_values

def get_slope_error(df):
	values_col = df.columns[0]
	df.index = pd.to_datetime(df.index)
	df[values_col] = pd.to_numeric(df[values_col])
	slope, intercept, rvalue, pvalue, stderr = scipy.stats.linregress(list(range(0,len(df))), df[values_col])
	return slope, stderr
