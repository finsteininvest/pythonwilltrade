'''
	get_sp_500.py

	Programm um die Symbole der aktullen
	Mitglieder des S&P 500 Index aus
	Wikipedia zu ermitteln.
	Ich setzte auf die Arbeit von
	Coding is Fun auf:
	https://codingandfun.com/python-scraping-how-to-get-sp-500-companies-from-wikipedia/

	Die Liste wird als csv gespeichert.

	Erstellt: März 2020

	https://finsteininvest.pythonanywhere.com/
'''

import bs4 as bs
import requests
import pandas as pd

resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(resp.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})

tickers_list = []


for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text.strip()
    name = row.findAll('td')[1].text.strip()
    industry = row.findAll('td')[4].text.strip()
    
    tickers_list.append([ticker,name,industry])

members_df = pd.DataFrame.from_records(tickers_list, columns=['ticker','name','industry'])
members_df.to_csv('sp500_members.csv', index=False)
