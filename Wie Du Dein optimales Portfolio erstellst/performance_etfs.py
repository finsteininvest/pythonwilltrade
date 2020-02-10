'''
	performance_etfs.py

	Programm, um:
	a) Die historischen Kurse von ETFs herunterzuladen,
	b) Deren Performance nach Gewichtung zu ermitteln,
	c) Die optimale Gewichtung nach Efficient Frontier zu ermitteln.

	Januar, Februar 2020
'''

from bs4 import BeautifulSoup
import numpy as np
import quantstats as qs
import argparse
import os
import re
import requests
import json
import pickle
import time
from datetime import datetime
import pandas as pd
import progress
import matplotlib.pyplot as plt

def lade_isin_datei(dateiname):
	# Function, um die ISIN Liste und Gewichte aus einer
	# CSV Datei zu laden.
	# Die CSV Datei muss das Format haben:
	# ISIN;Gewicht
	# wobei Gewicht in Dezimal angegeben wird, also
	# z.B.: 0.5 = 50%
	# Gewicht muss auf jeden Fall angegeben werden,
	# unter Umständen überall 0.00 eintragen.
	# Obacht, nicht ',' sonden '.'!
	isin_liste = []
	isin_liste_gewichte = []
	with open(dateiname, "r") as infile:
		for line in infile:
			m = re.search('(.*);(.*)', str(line))
			try:
				ISIN = m.group(1)
				Gewicht = m.group(2)
				isin_liste.append(ISIN)
				isin_liste_gewichte.append(float(Gewicht))
			except:
				# Ist die Datei falsch formatiert
				# wird die weitere Bearbeitung abgebrochen
				print('ISIN Datei fehlerhaft')
				print('Programm abgebrochen')
				quit()
	return isin_liste, isin_liste_gewichte

def lade_kurse(isin_liste):
    # Historische Kurse von ExtraEtf.com herunterladen
    # Es wird TRINAV gespeichert. Das sind die Kurse, inkl.
    # Ausschüttungen. (Falls nicht thesaurierend)
    # Die Daten werden als Pickle gespeichert.
    for isin in isin_liste:
        print(f'Downloading historical prices {isin}')
        etf_kurse = requests.get(f'https://de.extraetf.com/api-v2/chart/?isin={isin}&currency_id=2')
        parsed = json.loads(etf_kurse.text)
        results = parsed['results']
        for result, kurse in results.items():
            if result == 'trinav':
                #print(f'Kurse für {isin} werden gespeichert')
                pickle.dump( kurse, open( f'{isin}.p', "wb" ) )
        time.sleep(5)

def ermittel_eff(df_werte):
	# Code copied from here: https://towardsdatascience.com/python-markowitz-optimization-b5e1623060f5

    log_ret = np.log(df_werte/df_werte.shift(1))
    np.random.seed(42)
    num_ports = 50000
    all_weights = np.zeros((num_ports, len(log_ret.columns)))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)

    for x in range(num_ports):
        # Fortschritt
        progress.print_progress(x, num_ports)

        # Weights
        weights = np.array(np.random.random(len(log_ret.columns)))
        weights = weights/np.sum(weights)
            
        # Save weights
        all_weights[x,:] = weights
            
        # Expected return
        ret_arr[x] = np.sum( (log_ret.mean() * weights * 252))
            
        # Expected volatility
        vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
            
        # Sharpe Ratio
        sharpe_arr[x] = ret_arr[x]/vol_arr[x]
    print('\n\n')
    print(f'Max sharpe {sharpe_arr.max()}')
    print(f'Sharpe location {sharpe_arr.argmax()}')
    print(f'Weights {all_weights[sharpe_arr.argmax()]*100}')

    max_sr_ret = ret_arr[sharpe_arr.argmax()]
    max_sr_vol = vol_arr[sharpe_arr.argmax()]

    #plt.figure(figsize=(12,8))
    my_dpi=96
    plt.figure(figsize=(800/my_dpi, 600/my_dpi), dpi=my_dpi)
    plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.scatter(max_sr_vol, max_sr_ret,c='red', s=50) # red dot
    plt.show()

    # End of code copied from here: https://towardsdatascience.com/python-markowitz-optimization-b5e1623060f5

    return all_weights[sharpe_arr.argmax()]

def ermittel_kurse(erster_tag, kurse_datei):
    # Funktion, um die Kurse eines ETF zu umzuwandeln.
    # erster_tag muss das Format haben: YYYY-MM-TT
    erster_tag = datetime.strptime(erster_tag, '%Y-%m-%d')
    kurse_raw_list = pickle.load(open( f'{kurse_datei}.p', "rb" ))
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
        # Sonst funtioniert die Auswertung mit quantstats
        # nicht.
        dt_datum_wert = datetime.strptime(datum_wert, '%Y-%m-%d')
        # Nur die Kurse nach dem Starttag einlesen.
        if dt_datum_wert >= erster_tag:
            kurse_datum.append(dt_datum_wert)
            kurse_wert.append(float(close_wert))
            
    # Aus den Kursen eine Pandas Serie erstellen
    # Braucht quantstats
    df = pd.Series(kurse_wert,index = kurse_datum, name = f'{kurse_datei}')
    # Wir brauchen die täglichen % Änderungen
    #df_cum_returns = df.pct_change()
    return(df)


if __name__ == "__main__":

	# Create command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--load', help='Lade Kurse der ETF', required= False, default=False, action="store_true")
    parser.add_argument('-w', '--weights', help='Benutze Gewichtung in Datei', required= False, default=False, action="store_true")
    parser.add_argument('-e', '--eff', help='Ermittel optimale Gewichtung', required=False, default=False, action="store_true")
    parser.add_argument('-d', '--datei', help='Datei mit ISIN und Gewichtung', required=True)
    parser.add_argument('-p', '--performance', help='Berechne Portfolio Performance', required= False, action="store_true")
    parser.add_argument('-t', '--erster_tag', help='Erster Tag für die Berechnung (JJJJ-MM-TT)', required=False, default="2014-01-01")
    args = parser.parse_args()
    df_all_etf_kurse = pd.DataFrame()
    isin_liste, isin_liste_gewichte = lade_isin_datei(args.datei)
    
    if args.load:
        # Funktioniert
        # Kurse werden von ExtraETF heruntergeladen.
        # Es sind die Bruttowerte, also beinhalten die Ausschüttungen.
    	lade_kurse(isin_liste)
    if args.performance:

        for isin in isin_liste:
            df_kurse = ermittel_kurse(args.erster_tag,isin)
            df_all_etf_kurse[f'{isin}'] = df_kurse
        df_all_etf_kurse = df_all_etf_kurse.dropna()
        cols = list(df_all_etf_kurse.columns)

        #print(df_all_etf_kurse.to_string())
        #quit()

        # Ohne weights parameter wird eine Gleichgewichtung
        # der ETF angenommen
        series_list = [1/len(cols)]*len(cols)
        weights = pd.Series(series_list, index = cols)
        df_all_etf_kurse_ungewichtet = df_all_etf_kurse * weights
        df_all_etf_kurse_ungewichtet_summe = df_all_etf_kurse_ungewichtet.sum(axis=1)
        
        if args.eff == True and args.weights == True:
            weights = pd.Series(isin_liste_gewichte, index = cols)
            df_all_etf_kurse_benchmark = df_all_etf_kurse * weights
            df_all_etf_kurse_benchmark_summe = df_all_etf_kurse_benchmark.sum(axis=1)

            weights = ermittel_eff(df_all_etf_kurse)
            df_all_etf_kurse_gewichtet = df_all_etf_kurse * weights
            df_all_etf_kurse_gewichtet_summe = df_all_etf_kurse_gewichtet.sum(axis=1)
            qs.reports.html(df_all_etf_kurse_gewichtet_summe, df_all_etf_kurse_benchmark_summe, output = "performance_mit_benchmark.html", title = "EFF Portfolio vs. Gew. Portfolio")

        if args.eff == True and args.weights == False:
            weights = ermittel_eff(df_all_etf_kurse)
            df_all_etf_kurse_gewichtet = df_all_etf_kurse * weights
            df_all_etf_kurse_gewichtet_summe = df_all_etf_kurse_gewichtet.sum(axis=1)
            qs.reports.html(df_all_etf_kurse_gewichtet_summe, df_all_etf_kurse_ungewichtet_summe, output = "performance_mit_benchmark.html", title = "Gew. Portfolio vs. Benchmark")

        if args.eff == False and args.weights == True:
            weights = pd.Series(isin_liste_gewichte, index = cols)
            df_all_etf_kurse_gewichtet = df_all_etf_kurse * weights
            df_all_etf_kurse_gewichtet_summe = df_all_etf_kurse_gewichtet.sum(axis=1)
            qs.reports.html(df_all_etf_kurse_gewichtet_summe, df_all_etf_kurse_ungewichtet_summe, output = "performance_mit_benchmark.html", title = "Gew. Portfolio vs. Benchmark")
        
        if args.eff == False and args.weights == False:
            qs.reports.html(df_all_etf_kurse_ungewichtet_summe, output = "performance.html", title = "Performancebericht")
        
        
   