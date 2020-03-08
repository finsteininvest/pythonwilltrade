'''
	get_sp_500_dcf.py

	Programm, um die dcf Werte für eine Liste von Symbolen
	von herunterzuladen.
	Die Liste wird geordnet (von günstig bis weniger günstig)
	in der Datei sp_500_dcf.csv abgespeichert.

	Erstellt: März 2020

	https://finsteininvest.pythonanywhere.com/
'''

import pandas as pd
import requests
import argparse
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--symbols_file', help='Name of symbols csv file', required = True)
args = parser.parse_args()

symbole_df = pd.read_csv(args.symbols_file)

dcf_delta_list = []

for index, row in symbole_df.iterrows():
    ticker = row['ticker']
    name = row['name']
    dcf_json = requests.get(f"https://financialmodelingprep.com/api/v3/company/discounted-cash-flow/{ticker}")
    dcf_json = dcf_json.json()
    # Nicht für jeden Wert gibt es eine DCF Berechnung
    try:
        delta = float(dcf_json['dcf']) - float(dcf_json['Stock Price'])
        delta_prc = delta/float(dcf_json['Stock Price'])*100
        print(f"{name}, DCF: {dcf_json['dcf']}, latest close: {dcf_json['Stock Price']}, Delta: {delta}, {delta_prc}%")
        dcf_delta_list.append([name, ticker, dcf_json['dcf'], dcf_json['Stock Price'], delta, delta_prc])
        sleep(1)
    except:
        pass

dcf_delta_df = pd.DataFrame.from_records(dcf_delta_list, columns=['name','ticker','dcf', 'latest', 'delta', '%'])
dcf_delta_df = dcf_delta_df.sort_values(by=['%'], ascending = False)
dcf_delta_df.to_csv('sp_500_dcf.csv', sep = ';', decimal = ',')
