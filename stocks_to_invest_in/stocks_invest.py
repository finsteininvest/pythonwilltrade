'''
	stocks_invest.py

	Programm, um Aktien aus dem S&P 500
	zu finden, die
	a) günstig bewertet sind dcf > aktueller Marktwert,
	b) cash haben,
	c) gute Dividenden zahlen.


	April 2020

	https://finsteininvest.pythonanywhere.com/
'''

import fmp
import csv

asset_data_list = []

with open("sp_500_dcf.csv", 'r') as file_in:
	next(file_in)
	for line in file_in:
		num,name,ticker,dcf,latest,delta,prct = line.split(';')
		latest = latest.replace(',','.')
		print(f'Checking {name}')
		# Nicht alle zahlen eine Dividende
		try:
			dividends = fmp.get_historic_dividend(ticker)
			last_dividend = dividends[-1:]
			dividend = last_dividend['adjDividend']
		except:
			dividend = 0

		div_yield = float(dividend) / float(latest)

		balance_sheet_values = fmp.get_balance_sheet(ticker)
		try:
			current_assets = float(balance_sheet_values[-1:]['Total current assets'][0])
		except:
			current_assets = 0
		try:
			current_liabilities = float(balance_sheet_values[-1:]['Total current liabilities'][0])
		except:
			current_liabilities = 0
		try:
			cash = float(balance_sheet_values[-1:]['Cash and cash equivalents'][0])
		except:
			cash = 0
		try:
			recievables = float(balance_sheet_values[-1:]['Receivables'][0])
		except:
			recievables = 0
		
		working_capital = current_assets - current_liabilities
		try:
			current_ratio = current_assets / current_liabilities
		except:
			current_ratio = 0
		try:
			quick_ratio = (cash+recievables)/current_liabilities
		except:
			quick_ratio = 0
		try:
			cash_ratio = cash / current_liabilities
		except:
			cash_ratio = 0
		
		asset_data_list.append([name,ticker,latest,dcf,div_yield,working_capital,current_ratio,quick_ratio,cash_ratio])

with open('aktien_liste.csv', 'w') as myfile:
	myfile.write(f'name,ticker,latest,dcf,div_yield,working_capital,current_ratio,quick_ratio,cash_ratio\n')
	for asset in asset_data_list:
		name,ticker,latest,dcf,div_yield,working_capital,current_ratio,quick_ratio,cash_ratio = asset
		name = name.replace(',',' ')
		myfile.write(f'{name},{ticker},{latest},{dcf},{div_yield},{working_capital},{current_ratio},{quick_ratio},{cash_ratio}\n')