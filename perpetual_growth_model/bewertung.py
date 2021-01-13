'''
	bewertung.py

	Programm, um eine Aktie nach dem
	Modell des ewigen Wachstums
	zu bewerten.

	Es nutzt die API von financialmodelingprep.com
'''

import argparse
import requests
import json
import pandas as pd

apikey = ''

def get_dividends_annual(ticker, years):
	'''Function to retrieve dividends for
	   a given ticker.
	   It aggregates annualy and dismisses any data
	   outside the years range. It will also dismiss the
	   current year as stocks in the US
	   payout quarterly.

	'''
	years = int(years)
	url = f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{ticker}?apikey={apikey}'
	r = requests.get(url)
	json_data = json.loads(r.text)
	historical_dividends = pd.DataFrame.from_dict(json_data['historical'])
	historical_dividends = historical_dividends.sort_values(by='date')
	historical_dividends['date'] = pd.to_datetime(historical_dividends['date'])
	historical_dividends = historical_dividends.set_index('date')
	series_annual_dividends = historical_dividends.dividend.resample('Y').sum()

	df_annual_dividends = series_annual_dividends.to_frame()
	df_annual_dividends['growth'] = df_annual_dividends.pct_change()
	df_annual_dividends = df_annual_dividends[-years-1:-1]
	mean_growth = df_annual_dividends['growth'].mean()
	print(df_annual_dividends)
	print(f'Average dividend growth rate: {mean_growth*100:0.2f}')


def calc_perpetual_growth_model(dividend, growth, min_accepted_rate_of_return):
	'''Function to calcualte the value of a stock
	   based on the
	   Perpetual Growth Model

	'''

	v = (float(dividend) * (1+float(growth))) / (float(min_accepted_rate_of_return) - float(growth))
	print(f'Perpetual Growth Model Value: {v:0.2f}')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--ticker', required = False, help = 'Ticker of stock to evaluate')
	parser.add_argument('-y', '--years', default = 5, required = False, help = 'How many years to use for average calculation')
	parser.add_argument('-d', '--dividend', required = False, help = 'Current dividend')
	parser.add_argument('-g', '--growth', required = False, help = 'Stock growth rate')
	parser.add_argument('-m', '--min_accepted_rate_of_return', required = False, help = 'Stock growth rate')

	args = parser.parse_args()

	if args.ticker:
		get_dividends_annual(args.ticker, args.years)

	if args.dividend and args.growth and args.min_accepted_rate_of_return:
		calc_perpetual_growth_model(args.dividend, args.growth, args.min_accepted_rate_of_return)
