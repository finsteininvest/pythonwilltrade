'''
	etf_eoy_perf.py

	Programm, um die jährliche
	Performance eines ETFs zu ermitteln.

	Nutzt Dateien, die von consors_extract.py
	erstellt werden.

	Januar 2020

	https://finsteininvest.pythonanywhere.com
    https://git...
'''

import pickle
import argparse
import pandas as pd
from datetime import datetime
import os
import tabulate

def identify_eoy_for_all_etf():
	alle_etf = pd.DataFrame()
	alle_etf_isin = []
	for (dirname, dirs, files) in os.walk(os.getcwd()):     
		for filename in files:
			if filename.endswith('.p'):
				print(filename)
				df = identify_eoy_for_single_etf(filename)
				alle_etf = pd.concat([alle_etf, df],ignore_index=True)
				alle_etf_isin.append(filename.replace('.p', ''))
	alle_etf = alle_etf.drop(columns= pd.to_datetime('2020-12-31'))
	alle_etf['isin'] = alle_etf_isin
	return alle_etf


def identify_eoy_for_single_etf(kursdatei):
	kurse_raw_list = pickle.load(open( f'{kursdatei}', "rb" ))
	kurse_datum = []
	kurse_wert = []

	# Die Kurse von extraetf haben ein spezielles Format.
	# Hier erfolgt die Umwandlung
	for eintrag in kurse_raw_list:
		datum, wert = eintrag.items()
		datum_tag, datum_wert = datum
		close_tag, close_wert = wert
		# Werte mit Datum extrahiert,
		# Jetzt Datum in ein Python Datum umwandeln.
		dt_datum_wert = datetime.strptime(datum_wert, '%Y-%m-%d')
		kurse_datum.append(dt_datum_wert)
		kurse_wert.append(float(close_wert))
			
	# Aus den Kursen eine Pandas Serie erstellen
	df = pd.Series(kurse_wert,index = kurse_datum)

	df_annual = df.resample('Y').last()
	df_annual_pct = df_annual.pct_change()*100
	#print(df)
	df_annual_pct = df_annual_pct.dropna()
	df = pd.DataFrame(df_annual_pct)
	df = df.transpose()
	return df

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-k', '--kurse', help='Pickle Datei mit den Kursen', required=False)
	parser.add_argument('-w', '--walk', help='EOY Werte für alle Kursdateien ermitteln', required=False, default=False, action='store_true')
	args = parser.parse_args()
	if args.kurse:
		identify_eoy_for_single_etf(args.kurse)
	if args.walk:
		df = identify_eoy_for_all_etf()
		df.to_csv('etf_eoy_perf.csv', decimal = ',', sep = ';')
