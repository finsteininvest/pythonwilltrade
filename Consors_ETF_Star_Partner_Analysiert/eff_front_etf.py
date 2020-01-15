'''
	eff_front_etf.py

	Programm, um ein efficient frontier portfolio
	aus ETFs zu ermitteln.

	Januar 2020
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import progress
import quantstats as qs

def parse_date(datestr):
	year= int(datestr[6:10])
	month= int(datestr[3:5])
	day= int(datestr[0:2])
	return pd.datetime(year, month, day)

ETFs = ['LU0533033667',  'FR0011550185',  'IE00B53L4350',  'LU0533033238', 'IE0032895942']

erster_tag = datetime.strptime('2014-01-01', '%Y-%m-%d')
kurse_datum = [None]*len(ETFs)
kurse_wert = [None]*len(ETFs)

for num, ETF in enumerate(ETFs):
	print(f'Lade Kurse für {ETF}')
	kurse_datum[num] = []
	kurse_wert[num] = []
	kurse_raw_list = pickle.load(open( f'{ETF}.p', "rb" ))
	for eintrag in kurse_raw_list:
		datum, wert = eintrag.items()
		datum_tag, datum_wert = datum
		close_tag, close_wert = wert
		# Werte mit Datum extrahiert,
		# Jetzt Datum in ein Python Datum umwandeln.
		dt_datum_wert = datetime.strptime(datum_wert, '%Y-%m-%d')
		# Nur die Kurse nach dem Starttag einlesen.
		if dt_datum_wert >= erster_tag:
			kurse_datum[num].append(dt_datum_wert)
			kurse_wert[num].append(float(close_wert))

# Für weitere Umwandlungen werden die ganzen Listen im ein DataFrame umgewandelt.
df_werte = pd.DataFrame(list(zip(kurse_datum[0], kurse_wert[0],kurse_wert[1],kurse_wert[2],kurse_wert[3],kurse_wert[4])), columns = ['Datum', f'{ETFs[0]}',	f'{ETFs[1]}',	f'{ETFs[2]}',	f'{ETFs[3]}', f'{ETFs[4]}'])
df_werte = df_werte.set_index('Datum')

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
	weights = np.array(np.random.random(len(ETFs)))
	weights = weights/np.sum(weights)
	    
	# Save weights
	all_weights[x,:] = weights
	    
	# Expected return
	ret_arr[x] = np.sum( (log_ret.mean() * weights * 252))
	    
	# Expected volatility
	vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
	    
	# Sharpe Ratio
	sharpe_arr[x] = ret_arr[x]/vol_arr[x]

print('\n')
print(f'Max sharpe {sharpe_arr.max()}')
print(f'Sharpe location {sharpe_arr.argmax()}')
print(f'Weights {all_weights[sharpe_arr.argmax()]}')

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

# Performance gewichtet
etf_1_weight,etf_2_weight,etf_3_weight,etf_4_weight,etf_5_weight = all_weights[sharpe_arr.argmax()]
df_werte['Portfolio_Gew'] = df_werte[f'{ETFs[0]}']*etf_1_weight + df_werte[f'{ETFs[1]}']*etf_2_weight + df_werte[f'{ETFs[2]}']*etf_3_weight + df_werte[f'{ETFs[3]}']*etf_4_weight + df_werte[f'{ETFs[4]}']*etf_5_weight
# Aus den Kursen eine Pandas Serie erstellen
# Braucht qunatstats
df = pd.Series(df_werte['Portfolio_Gew'].values.tolist(), index = df_werte.index)
# Wir brauchen die täglichen % Änderungen
df_cum_returns_weight = df.pct_change()

# Benchmark: MSCI Welt
df_msci = pd.read_csv('msci_welt.csv', sep = ';', thousands = '.', decimal = ',', date_parser = parse_date, parse_dates=['Datum'])
df_msci = df_msci.set_index('Datum')
# Aus den Kursen eine Pandas Serie erstellen
# Braucht quantstats
df = pd.Series(df_msci['Schluss'].values.tolist(), index = df_msci.index)
# Wir brauchen die täglichen % Änderungen
df_cum_returns = df.pct_change()

# Einen vollen HTML Bericht erzeugen.
datei = 'EFFETF.html'
titel = 'Optimales Consors ETF Portfolio'
qs.reports.html(df_cum_returns_weight, df_cum_returns, output = datei, title = titel)