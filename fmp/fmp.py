'''
	fmp.py

	Sammlung von Funktionen, um
	Daten von financialmodelingprep
	herunterzuladen.

	Erstellt: 1. März 2020
	Erweitert: 12. März 2020
	Erweitert: 23. März 2020
		- creation_date_today
		- check_cache
		- einige Funktionen nutzen nun check_cache.
		  In Vorbereitung zur Nutzung mit FMP Dashboard
	Erweitert: 01. April 2020
		- Neu get_balance_sheet
	Reweitert: 
		- Neue Funktionen
		- Weitere Funktionen nutzen nun check_cache.

	https://finsteininvest.pythonanywhere.com/
	https://github.com/finsteininvest/pythonwilltrade/tree/master/fmp
	
	Nutzt: https://financialmodelingprep.com/
'''

import json
import requests
import pandas as pd
import scipy
from scipy import stats
import pickle
import os
import time
import platform
from pathlib import Path
from datetime import date

def creation_date_today(path_to_file):
	'''
	    Function to check if a file exists and if it was
	    created today
	'''
	check_file = Path(path_to_file)
	if check_file.exists():
		today_split = date.today().strftime('%c').split(' ')
		touched_split = time.ctime(os.path.getctime(path_to_file)).split(' ')
		today = today_split[1]+today_split[2]+today_split[4]
		touched = touched_split[1]+touched_split[2]+touched_split[4]
		if today == touched:
			return True
		else:
			return False
	else:
		return False

def check_cache(query):
	'''
		Function to check if a query has been made today to a web page.
		In that case the cached query is returned.
		Otherwise; excute the query and cache it
	'''
	file_name_parts = query.split('/')
	file_name = file_name_parts[-2] + '_' + file_name_parts[-1] 
	r = ''
	if creation_date_today(file_name):
		r = pickle.load(open(file_name, 'rb'))
	else:
		r = requests.get(query)
		pickle.dump(r, open(file_name, 'wb'))
	return r


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
	r = check_cache('https://financialmodelingprep.com/api/v3/company/stock/list')
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
	r = check_cache(f'https://financialmodelingprep.com/api/v3/historical-price-full/{type}{symbol}?apikey=fd02372d10ae6e79e2f270de31bd55a6')
	historic_list = json.loads(r.text)
	if debug == True:
		for entry in historic_list['historical']:
			print(entry['date'])

	historic_values = pd.DataFrame.from_dict(historic_list['historical'])
	historic_values = historic_values.sort_values(by=['date'])
	historic_values = historic_values.set_index('date')

	return historic_values

def get_dcf(symbol):
	'''
		Gets latest DCF and price
		Returns two values
		dcf, price
	'''
	r = check_cache(f'https://financialmodelingprep.com/api/v3/company/discounted-cash-flow/{symbol}?apikey=fd02372d10ae6e79e2f270de31bd55a6')
	historic_dcf = json.loads(r.text)
	dcf = historic_dcf['dcf']
	price = historic_dcf['Stock Price']

	return dcf, price

def get_historic_eps(symbol, debug=False):
	'''
		Retrieves a dataframe for eps
		for a given symbol.

		Index is set to date
	'''
	r = check_cache(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{symbol}?apikey=fd02372d10ae6e79e2f270de31bd55a6')
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
		Retrieves a dataframe for ROE
		for a given symbol.

		Index is set to date
	'''
	r = check_cache(f'https://financialmodelingprep.com/api/v3/company-key-metrics/{symbol}?apikey=fd02372d10ae6e79e2f270de31bd55a6')
	historic_roe_value_list = json.loads(r.text)
	if debug == True:
		for entry in historic_roe_value_list['metrics']:
			print(entry['date'])
	historic_roe_values = pd.DataFrame.from_dict(historic_roe_value_list['metrics'])
	historic_roe_values = historic_roe_values.sort_values(by=['date'])
	historic_roe_values = historic_roe_values[['date', 'ROE']]
	historic_roe_values['ROE'] = historic_roe_values['ROE'].astype(float) * 100
	historic_roe_values = historic_roe_values.set_index('date')

	return historic_roe_values

def get_historic_dividend(symbol, debug = False):
	'''
		Retrieves a dataframe for dividends
		for a given symbol.

		Index is set to date
	'''
	r = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{symbol}?apikey=fd02372d10ae6e79e2f270de31bd55a6')
	historic_dividend_list = json.loads(r.text)
	if debug == True:
		for entry in historic_dividend_list['historical']:
			print(entry['date'])
	try:
		historic_dividend_values = pd.DataFrame.from_dict(historic_dividend_list['historical'])
		historic_dividend_values = historic_dividend_values.sort_values(by=['date'])
		historic_dividend_values = historic_dividend_values[['date', 'adjDividend']]
		historic_dividend_values['date'] = pd.to_datetime(historic_dividend_values['date'])
		historic_dividend_values = historic_dividend_values.set_index('date')
		historic_dividend_values = historic_dividend_values.resample('Y').sum()
		return historic_dividend_values
	except:
		return 0

def get_book_value_per_share(symbol, debug = False):
	'''
		Retrieves a dataframe for book value per share
		for a given symbol.

		Index is set to date
	'''
	r = requests.get(f'https://financialmodelingprep.com/api/v3/company-key-metrics/{symbol}?apikey=fd02372d10ae6e79e2f270de31bd55a6')
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
	'''
		Calculates slope and error for
		a dataframe.
		Dataframe should have date as index and
		the values to use in column 0.

		Returns a tuple for slope and stderr.
	'''
	values_col = df.columns[0]
	df.index = pd.to_datetime(df.index)
	df[values_col] = pd.to_numeric(df[values_col])
	slope, intercept, rvalue, pvalue, stderr = scipy.stats.linregress(list(range(0,len(df))), df[values_col])
	return slope, stderr

def get_balance_sheet(symbol, debug = False):
	'''
		Retrieves dataframe with balance sheet
		data available (for the last 10 years?)

		Index is set to date
	'''
	r = check_cache(f'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{symbol}?apikey=fd02372d10ae6e79e2f270de31bd55a6')
	balance_sheet_value_list = json.loads(r.text)
	if debug == True:
		for entry in balance_sheet_value_list['financials']:
			print(entry['date'])
	balance_sheet_values = pd.DataFrame.from_dict(balance_sheet_value_list['financials'])
	balance_sheet_values = balance_sheet_values.sort_values(by=['date'])
	balance_sheet_values = balance_sheet_values.set_index('date')

	return balance_sheet_values

def get_debt_equity(symbol):
	'''
		Retrieves dataframe with debt and equity
		and the debt/equity ratio

		Index is set to date
	'''
	balance_sheet_values = get_balance_sheet(symbol)

	try:
		debt_equity = balance_sheet_values[['Total debt', 'Total shareholders equity']]
		debt_equity = debt_equity[['Total debt','Total shareholders equity']].astype(float)
		debt_equity['de_ratio'] = debt_equity['Total debt'] / debt_equity['Total shareholders equity']
		return debt_equity
	except:
		return 0

def get_net_income(symbol):
	return 0

def get_current_ratio(symbol):
	'''
		Retrieves dataframe with assets and liabilities
		and the current ratio

		Index is set to date
	'''
	balance_sheet_values = get_balance_sheet(symbol)
	try:
		current = balance_sheet_values[['Total current assets','Total current liabilities']].astype(float)
		current['current_ratio'] = current['Total current assets'] / current['Total current liabilities']
		return current
	except:
		return 0

def get_number_shares_outstanding(symbol):
	'''
		Retrieves dataframe with numbers of shares
		over time

		Index is set to date
	'''
	r = check_cache(f'https://financialmodelingprep.com/api/v3/enterprise-value/{symbol}?apikey=fd02372d10ae6e79e2f270de31bd55a6')
	outstanding_shares_list = json.loads(r.text)
	try:
		outstanding_shares_temp = pd.DataFrame.from_dict(outstanding_shares_list['enterpriseValues'])
		outstanding_shares = outstanding_shares_temp[['date','Number of Shares']]
		outstanding_shares = outstanding_shares.sort_values(by=['date'])
		outstanding_shares = outstanding_shares.set_index('date')
		return outstanding_shares
	except:
		return 0

def get_earnings_before_tax(symbol):
	'''
		Retrieves dataframe with earnings before tax
		over time

		Index is set to date
	'''
	r = check_cache(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{symbol}?apikey=fd02372d10ae6e79e2f270de31bd55a6')
	historic_earnings_list = json.loads(r.text)

	historic_earnings_list_temp = pd.DataFrame.from_dict(historic_earnings_list['financials'])
	historic_earnings = historic_earnings_list_temp.sort_values(by=['date'])
	historic_earnings = historic_earnings[['date', 'Earnings before Tax']]
	historic_earnings = historic_earnings.sort_values(by=['date'])
	historic_earnings = historic_earnings.set_index('date')

	return historic_earnings

def get_current_quick_cash(symbol):
	return 0


def get_net_income(symbol):
	'''
		Retrieves a dataframe of net income.

		Index is set to date
	'''
	r = check_cache(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{symbol}?apikey=fd02372d10ae6e79e2f270de31bd55a6')
	historic_income_list = json.loads(r.text)

	historic_income_list_temp = pd.DataFrame.from_dict(historic_income_list['financials'])
	historic_income = historic_income_list_temp.sort_values(by=['date'])
	historic_income = historic_income[['date', 'Net Income']]
	historic_income = historic_income.sort_values(by=['date'])
	historic_income = historic_income.set_index('date')

	return historic_income
	
def get_price_earning_ratio(symbol):
	'''
		Retrieves a single value:
		Price/Earnings ratio
	'''
	net_income = get_net_income(symbol)[-1:]
	net_income = float(net_income.iloc[-1]['Net Income'])
	prices = get_historic_values(symbol, type = '')
	latest_close = float(prices[-1:]['close'])
	num_shares = get_number_shares_outstanding(symbol)[-1:]
	num_shares = float(num_shares.iloc[-1]['Number of Shares'])
	earnings_per_share = net_income / num_shares
	p_e = latest_close / earnings_per_share
	return p_e

def get_price_book_ratio(symbol):
	'''
		Retrieves a single value:
		Price/Book Ratio
	'''
	symbol = symbol + '?period=quarter'
	prices = get_historic_values(symbol, type = '')
	latest_close = float(prices[-1:]['close'])
	num_shares = get_number_shares_outstanding(symbol)[-1:]
	num_shares = float(num_shares.iloc[-1]['Number of Shares'])
	equity = get_debt_equity(symbol)
	latest_equity = float(equity[-1:]['Total shareholders equity'])
	book_value = latest_equity / num_shares
	p_b = latest_close / book_value
	return p_b
