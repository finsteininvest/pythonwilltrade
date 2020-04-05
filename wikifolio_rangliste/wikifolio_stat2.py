# -*- coding: utf-8 -*-
'''
	wikifolio_stat2.py
	
	Programm, um Statistiken von
	Wikifolios auszurechnen.

	Februar 2020

	Die HTML Datei wurde vorher gespeichert.
	Hierzu vorher auf der Homepage von wikifolio.de
	einloggen und Scuhergebnisse filtern.
	Zum Schluss die komplette HTML Seite speichern.

	Aufruf des Programms:
	python3 wikifolio_stat2.py -f wikif_perf.html
'''

from bs4 import BeautifulSoup
import re
import argparse
from prettytable import PrettyTable

# Parameter fuer die Kommandozeile definieren
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Wikifolio HTML file', required=True)
args = parser.parse_args()

# HTML Datei parsen
soup = BeautifulSoup(open(args.file, "r"), "html.parser")

# Einzelne Wikifolio Bloecke in der Datei identifizieren.
wikifolios = soup.find_all("div", class_="js-wf-preview__root")									  

# Tabelle fuer die Ausgabe vorbereiten
t = PrettyTable(['Rang','ISIN', 'Name', 'Investiert', 'Ø Perf.'])
rang = 1

# Fuer jedes Wikifolio die Werte auslesen
for wikifolio in wikifolios:
	name = wikifolio.find("a", class_="c-icon-name__text u-fw-sb gtm-wfpreview__title")
	# isin wird nicht in der Tabelle ausgegeben.
	isin = wikifolio.find("span", class_="js-copy-isin")
	investiert = wikifolio.find_all("span", class_="c-strike__value")
	investiert_eur = investiert[7].text.replace('EUR', '')
	wikifolio_name = name.text
	# Regulaeren Ausdruck verwenden, um Performance
	# zu ermitteln. Der Eintrag aendert sich, je nachdem ob
	# die Performance positiv oder negativ ist.
	#perf_pattern= re.compile("pull-right text-small text-bold rightspan u-.*")
	perf = wikifolio.find_all("span", class_="c-strike__value")
	perf = perf[2].text
	# Gefundene Werte in Tabelle eintragen
	t.add_row([str(rang), isin.text, wikifolio_name, investiert_eur, perf])
	t.align['Name'] = 'l'
	t.align['ISIN'] = 'l'
	t.align['Rang'] = 'r'
	t.align['Investiert'] = 'r'
	t.align['Ø Perf.'] = 'r'
	rang += 1

# Tabelle ausgeben
print(t)