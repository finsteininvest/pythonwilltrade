'''
    performance_aktien.py

    Programm, um:
    a) Die historischen Kurse von Aktien herunterzuladen,
    b) Deren Performance nach Gewichtung zu ermitteln,
    c) Die optimale Gewichtung nach Efficient Frontier zu ermitteln.

    März 2020

    https://finsteininvest.pythonanywhere.com
'''

from bs4 import BeautifulSoup
import numpy as np
import quantstats as qs
import argparse
import re
import requests
import json
import time
from datetime import datetime
import pandas as pd
import progress
import matplotlib.pyplot as plt
import fmp
import pandas_datareader as pdr

def lade_symbol_datei(dateiname):
    '''
       Function, um die Symbol Liste und Gewichte aus einer
       CSV Datei zu laden.
       Die CSV Datei muss das Format haben:
       ISIN;Gewicht
       wobei Gewicht in Dezimal angegeben wird, also
       z.B.: 0.5 = 50%
       Gewicht muss auf jeden Fall angegeben werden,
       unter Umständen überall 0.00 eintragen.
       Obacht, nicht ',' sonden '.'!
    '''
    symbol_liste = []
    symbol_liste_gewichte = []
    with open(dateiname, "r") as infile:
        for line in infile:
            m = re.search('(.*);(.*)', str(line))
            try:
                symbol = m.group(1)
                Gewicht = m.group(2)
                symbol_liste.append(symbol)
                symbol_liste_gewichte.append(float(Gewicht))
            except:
                # Ist die Datei falsch formatiert
                # wird die weitere Bearbeitung abgebrochen
                print('Symbol Datei fehlerhaft')
                print('Programm abgebrochen')
                quit()
    return symbol_liste, symbol_liste_gewichte

def lade_kurse_stooq(symbol_liste):
    '''
        Funktion, um Kurse von
        Yahoo Finance herunterzuladen.
        Kurse werden in einer CSV Datei gespeichert.
        Bsp. [symbol].csv
    '''
    for symbol in symbol_liste:
        print(f'Versuche Kursdaten für {symbol} zu laden')
        try:
            df_hist_close = pdr.stooq.StooqDailyReader(f'{symbol}').read()
            df_hist_close.to_csv(f'{symbol}.csv')
            print(f'Kursdaten für {symbol} gespeichert')
        except:
            pass
        time.sleep(5)

def lade_kurse_fmp(symbol_liste):
    '''
        Funktion, um Kurse von
        financialmodelingprep.com herunterzuladen.
        Kurse werden in einer CSV Datei gespeichert.
        Bsp. [symbol].csv
    '''
    for symbol in symbol_liste:
        print(f'Versuche Kursdaten für {symbol} zu laden')
        try:
            df_hist_close = fmp.get_historic_values(symbol, type='')
            df_hist_close.to_csv(f'{symbol}.csv')
            print(f'Kursdaten für {symbol} gespeichert')
        except:
            pass
        time.sleep(5)   

def ermittel_eff(df_werte):
    '''
        Funktion, um die optimalen Gewichte in einem
        Portfolio zu ermitteln.
    '''

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


def lade_kurse_datei(erster_tag, kurse_datei):
    # Funktion, um die Kurse eines Symbols zu umzuwandeln.
    # erster_tag muss das Format haben: YYYY-MM-TT
    erster_tag = datetime.strptime(erster_tag, '%Y-%m-%d')
    kurse_datum = []
    kurse_wert = []

    with open(f'{kurse_datei}.csv') as file_in:
        lines = []
        for line in file_in:
            if 'Close' not in line and 'close' not in line:
                items = line.split(',')
                close_wert = items[4]
                datum_wert = items[0]
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
    return(df)

if __name__ == "__main__":

    # Create command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--load_stooq', help='Lade Kurse von Stooq', required= False, default=False, action="store_true")
    parser.add_argument('-f', '--load_fmp', help='Lade Kurse von financialmodelingprep.com', required= False, default=False, action="store_true")
    parser.add_argument('-w', '--weights', help='Benutze Gewichtung in Datei', required= False, default=False, action="store_true")
    parser.add_argument('-e', '--eff', help='Ermittel optimale Gewichtung', required=False, default=False, action="store_true")
    parser.add_argument('-d', '--datei', help='Datei mit Symbol und Gewichtung', required=True)
    parser.add_argument('-p', '--performance', help='Berechne Portfolio Performance', required= False, action="store_true")
    parser.add_argument('-t', '--erster_tag', help='Erster Tag für die Berechnung (JJJJ-MM-TT)', required=False, default="2014-01-01")
    args = parser.parse_args()

    df_alle_kurse = pd.DataFrame()
    symbol_liste, symbol_liste_gewichte = lade_symbol_datei(args.datei)
    
    if args.load_stooq:
        lade_kurse_stooq(symbol_liste)
        print('Fertig')

    if args.load_fmp:
        lade_kurse_fmp(symbol_liste)
        print('Fertig')

    if args.performance:

        for symbol in symbol_liste:
            df_kurse = lade_kurse_datei(args.erster_tag,symbol)
            df_alle_kurse[f'{symbol}'] = df_kurse
        df_alle_kurse = df_alle_kurse.dropna()
        cols = list(df_alle_kurse.columns)


        # Ohne weights parameter wird eine Gleichgewichtung
        # angenommen
        series_list = [1/len(cols)]*len(cols)
        weights = pd.Series(series_list, index = cols)
        df_alle_kurse_ungewichtet = df_alle_kurse * weights
        df_alle_kurse_ungewichtet_summe = df_alle_kurse_ungewichtet.sum(axis=1)
        
        if args.eff == True and args.weights == True:
            weights = pd.Series(symbol_liste_gewichte, index = cols)
            df_all_etf_kurse_benchmark = df_all_etf_kurse * weights
            df_all_etf_kurse_benchmark_summe = df_all_etf_kurse_benchmark.sum(axis=1)

            weights = ermittel_eff(df_all_etf_kurse)
            df_all_etf_kurse_gewichtet = df_all_etf_kurse * weights
            df_all_etf_kurse_gewichtet_summe = df_all_etf_kurse_gewichtet.sum(axis=1)
            qs.reports.html(df_all_etf_kurse_gewichtet_summe, df_all_etf_kurse_benchmark_summe, output = "performance_mit_benchmark.html", title = "EFF Portfolio vs. Gew. Portfolio")

        if args.eff == True and args.weights == False:
            weights = ermittel_eff(df_alle_kurse)
            df_alle_kurse_gewichtet = df_alle_kurse * weights
            df_alle_kurse_gewichtet_summe = df_alle_kurse_gewichtet.sum(axis=1)
            qs.reports.html(df_alle_kurse_gewichtet_summe, df_alle_kurse_ungewichtet_summe, output = "performance_mit_benchmark.html", title = "Gew. Portfolio vs. Benchmark")

        if args.eff == False and args.weights == True:
            weights = pd.Series(symbol_liste_gewichte, index = cols)
            df_alle_kurse_gewichtet = df_alle_kurse * weights
            df_alle_kurse_gewichtet_summe = df_alle_kurse_gewichtet.sum(axis=1)
            qs.reports.html(df_alle_kurse_gewichtet_summe, df_alle_kurse_ungewichtet_summe, output = "performance_mit_benchmark.html", title = "Gew. Portfolio vs. Benchmark")
        
        if args.eff == False and args.weights == False:
            qs.reports.html(df_alle_kurse_ungewichtet_summe, output = "performance.html", title = "Performancebericht")
        
        
   