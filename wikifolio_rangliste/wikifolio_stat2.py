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

# Parameter für die Kommandozeile definieren
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Wikifolio HTML file', required=True)
args = parser.parse_args()

# HTML Datei parsen
soup = BeautifulSoup(open(args.file, "r"), "html.parser")

# Einzelne Wikifolio Blöcke in der Datei identifizieren.
wikifolios = soup.find_all("div", class_="container-fluid wikifolio-preview js-watchlist-wikifoliopreview c-search-card")									  

# Tabelle für die Ausgabe vorbereiten
t = PrettyTable(['Rang','ISIN', 'Name', 'Investiert', '1M Perf.'])
rang = 1

# Für jedes Wikifolio die Werte auslesen
for wikifolio in wikifolios:
	name = wikifolio.find("span", class_="js-wikifolio-shortdescription")
	# isin wird nicht in der Tabelle ausgegeben.
	isin = wikifolio.find("span", class_="js-copy-isin")
	investiert = wikifolio.find_all("span", class_="pull-right text-small text-bold rightspan")
	investiert_eur = investiert[5].text.replace('EUR', '')
	wikifolio_name = name.text

	# Regulären Ausdruck verwenden, um Performance
	# zu ermitteln. Der Eintrag ändert sich, je nachdem ob
	# die Performance positiv oder negativ ist.
	perf_pattern= re.compile("pull-right text-small text-bold rightspan u-.*")
	perf = wikifolio.find_all("span", perf_pattern)

	# Gefundene Werte in Tabelle eintragen
	t.add_row([str(rang), isin.text, wikifolio_name, investiert_eur, perf[1].text])
	t.align['Name'] = 'l'
	t.align['ISIN'] = 'l'
	t.align['Rang'] = 'r'
	t.align['Investiert'] = 'r'
	t.align['1M Perf.'] = 'r'
	rang += 1

# Tabelle ausgeben
print(t)
