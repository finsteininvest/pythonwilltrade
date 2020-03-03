'''
	plot_gc.py

	Programm, um eine Phase des Golden Cross
	als Chart zu zeichnen.

	März 2020

'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from datetime import datetime
import fmp


parser = argparse.ArgumentParser()

parser.add_argument('-i', '--symbol', help='Symbol', required=True)
parser.add_argument('-p', '--plot', help='Zeige Chart', required=False, action='store_true')
parser.add_argument('-s', '--save', help='Speicher Chart', required=False, action='store_true')
parser.add_argument('-t', '--type', help='Welche Art von Kursen', required=True)
args = parser.parse_args()

pd.plotting.register_matplotlib_converters()

# Daten einlesen
df = fmp.get_historic_values(args.symbol, type = args.type, debug = False)

# Tage ohne Wert werden gelöscht.
df = df.dropna()

# Gleitende Durchschnitte berechnen
df['sma20'] = df['close'].rolling(20).mean()
df['sma50'] = df['close'].rolling(50).mean()
df['sma200'] = df['close'].rolling(200).mean()
df['phase'] = np.nan
df['datum'] = df.index
phase = []

# Durch die Daten schleifen und für jeden Tag die Phase ermitteln.
for index, row in df.iterrows():
	phaseval = 0
	'''
	1.  Erholungsphase:
    	SMA 50 < SMA 200 und Schlusskurs < SMA 200 und Schlusskurs > SMA 50
    '''
	if row.sma50 < row.sma200 and row.close < row.sma200 and row.close > row.sma50:
		phaseval = 1
	'''
	2.  Akkummulationsphase:
		SMA 50 < SMA 200 und Schlusskurs > SMA 200 und Schlusskurs > SMA 50
	'''
	if row.sma50 < row.sma200 and row.close > row.sma200 and row.close > row.sma50:
		phaseval = 2
	'''
	3.  Bullenphase:
		SMA 50 > SMA 200 und Schlusskurs > SMA 200 und Schlusskurs > SMA 50
	'''
	if row.sma50 > row.sma200 and row.close > row.sma200 and row.close > row.sma50:
		phaseval = 3
	'''
	4.  Warnungsphase:
		SMA 50 > SMA 200 und Schlusskurs > SMA 200 und Schlusskurs < SMA 50
	'''
	if row.sma50 > row.sma200 and row.close > row.sma200 and row.close < row.sma50:
		phaseval = 4
	'''
	5.  Verteilungsphase:
		SMA 50 > SMA 200 und Schlusskurs < SMA 200 und Schlusskurs < SMA 50
	'''
	if row.sma50 > row.sma200 and row.close < row.sma200 and row.close < row.sma50:
		phaseval = 5
	'''
	6.  Bärenphase:
		SMA 50 < SMA 200 und Schlusskurs < SMA 200 und Schlusskurs < SMA 50
	'''	
	if row.sma50 < row.sma200 and row.close < row.sma200 and row.close < row.sma50:
		phaseval = 6
	phase.append(phaseval)

df['phase'] = phase
# Nur die letzten 200 Tage
df = df[-200:]

# Chartstil einstellen
plt.style.use('fivethirtyeight')

# Kurse zeichnen
lines = plt.plot_date(x=df.index, y=df['close'], fmt="k-")

# Die gleitenden Durchschnitte etwas dünner zeichnen lassen.
lines = plt.plot_date(x=df.index, y=df['sma20'], fmt="y-")
plt.setp(lines[0], linewidth=2)
lines = plt.plot_date(x=df.index, y=df['sma50'], fmt="g-")
plt.setp(lines[0], linewidth=2)
lines = plt.plot_date(x=df.index, y=df['sma200'], fmt="b-")
plt.setp(lines[0], linewidth=2)


# Phase einzeichnen. In diesem Fall nur Phase 3 = Bullenphase
st = 0
for i in range(1, len(df['close'])):
	if df['phase'].iloc[i] == 3 and df['phase'].iloc[i-1] != 3:
		st = i
	if df['phase'].iloc[i] != 3 and df['phase'].iloc[i-1] == 3:
		plt.axvspan(df['datum'].iloc[st], df['datum'].iloc[i], color='g', alpha=0.2, lw=0)
		st = 0
if df['phase'].iloc[i] == 3 and st > 0:
	plt.axvspan(df['datum'].iloc[st], df['datum'].iloc[i], color='g', alpha=0.2, lw=0)
# Chart beschriften
plt.xlabel('Datum')
plt.ylabel('Schlusskurs (€)')
plt.legend(('Schlusskurs', 'GD 20', 'GD 50', 'GD 200'))

ax = plt.gca()

# Auf der X-Achse nur jeden 5ten Tag anzeigen.
xticks = np.arange(0, 200, 5)
ax.set_xticks(xticks)

# Datumsangaben auf der x-Achse um 45 Grad drehen.
for label in ax.xaxis.get_ticklabels():
        label.set_rotation(45)
plt.suptitle(args.symbol)
plt.subplots_adjust(left=0.17, bottom=0.15, right=0.97, top=0.93, wspace=0.2, hspace=0)

if args.save:
	file_name = args.symbol.replace('/', '_')
	file_name = file_name.replace(' ', '_')
	file_name = file_name + '.png'
	plt.savefig(file_name, format='png', dpi=300)
if args.plot:
	plt.show()

print(df.iloc[-1])
#^GDAXI = Dax
#^N225 = Nikkei
#^FTSE = FTSE 100
#^FCHI = CAC40
#^DJI = Dow Jones
#^GSPC = S&P500
#^IXIC = Nasdaq