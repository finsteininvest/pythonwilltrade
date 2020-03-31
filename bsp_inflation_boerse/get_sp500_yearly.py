'''
	get_sp500_yearly.py

	Programm um die US BSP Daten
	von The Balance herunterzuladen

	März 2020

	https://finsteininvest.pythonanywhere.com/
'''

from bs4 import BeautifulSoup
import requests
import pandas as pd

resp = requests.get('https://www.macrotrends.net/2324/sp-500-historical-chart-data')
soup = BeautifulSoup(resp.text, 'html.parser')
table = soup.find('table')

years_list = []

def clean_number(str_number):
	str_number = str_number.replace(',','')
	str_number = str_number.replace('%','')
	return float(str_number)

for row in table.findAll('tr')[2:]:
	year = row.findAll('td')[0].text.strip()
	avg_close = clean_number(row.findAll('td')[1].text.strip())
	year_open = clean_number(row.findAll('td')[2].text.strip())
	high = clean_number(row.findAll('td')[3].text.strip())
	low = clean_number(row.findAll('td')[4].text.strip())
	close = clean_number(row.findAll('td')[5].text.strip())
	ann_change = clean_number(row.findAll('td')[6].text.strip())
	years_list.append([year,avg_close,year_open,high,low,close,ann_change])


members_df = pd.DataFrame.from_records(years_list, columns=['year','avg_close','year_open','high','low','close','ann_change'])
members_df.to_csv('sp_500_yearly.csv', index=False)