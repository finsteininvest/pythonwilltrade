'''
	get_monthly_dividend_stocks.py

	Programm, um die Liste der Assets
	(Aktien, Fonds, ETFS, ETC.)
	auszulesen, die montliche Dividenden
	ausschütten.


	Erstellt: März 2020
'''

import requests
from bs4 import BeautifulSoup
import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--datei', help='Symbol', required=True)
parser.add_argument('-s', '--stocks', help='Nur Aktien ausgeben', required=False, action='store_true')
args = parser.parse_args()

soup = BeautifulSoup(open(args.datei, "r"), "html.parser")

assets_table = soup.find("tbody")
assets = assets_table.find_all("tr")
asset_list = []
asset_labels = ['symbol', 'name', 'asset_type', 'div_yield', 'eps', 'pe_ratio']
for asset in assets:
	spalten = asset.find_all("td")
	symbol = spalten[0].find("div", class_ = "ticker-area").text
	name = spalten[0].find("div", class_ = "title-area").text
	asset_type = spalten[1].text
	div_yield = spalten[2].text
	eps =  spalten[6].text
	pe_ratio =  spalten[7].text
	asset_list.append([symbol, name, asset_type, div_yield, eps, pe_ratio])

df_assets = pd.DataFrame.from_records(asset_list, columns = asset_labels)


if args.stocks:
	df_assets = df_assets[df_assets['asset_type']=='Stock']
	print(df_assets.to_string())
else:
	print(df_assets.to_string())

df_assets.to_csv('dividenden.csv', sep = ';')


