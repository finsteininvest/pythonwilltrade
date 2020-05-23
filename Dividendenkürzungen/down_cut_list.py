'''
	down_cut_list.py

	Programm, um die aktuellen Veränderung
	an Dividendenzahlungen aus dem Internet
	heruntezuladen.

	Mai 2020
	https://finsteininvest.pythonanywhere.com
'''

import requests
from bs4 import BeautifulSoup

def down_cut_list():
	cut_list = []
	headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
	}
	src = requests.get('https://dividendpower.org/2020/03/27/coronavirus-dividend-cuts-and-suspensions-tracker/', headers=headers)
	soup = BeautifulSoup(src.text, "html.parser")
	table_rows = soup.find_all("tr")
	for row in table_rows:
		td_data = row.find_all("td")
		td_count = 0
		name = ''
		symbol = ''

		for td in td_data:

			if td_count == 0:
				name = td.text
			if td_count	== 1:
				symbol = td.text
			td_count += 1
		cut_list.append([name, symbol])

	return cut_list

if __name__ == '__main__':
	list = down_cut_list()
	with open('cut_list', 'w') as file:
		for name, symbol in list:
			if len(name) > 0:
				file.write(f'{name};{symbol}\n')
