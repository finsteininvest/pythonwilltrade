'''
	scrape_aww.py

	Programm, um Waldpreise zu ermitteln.
	Genutzt werden Daten der Seite:
	https://www.ackerwaldundwiese.de

	Schritt 1 bei der Ermittlung der
	Waldpreise in Deutschland.

	Erzeugt die Datei: aww_data.csv

	Siehe: https://finsteininvest.pythonanywhere.com/2019/12/21/was-kostet-ein-wald/

	Dezember 2018
	Aktualisiert Dezember 2019
'''

from bs4 import BeautifulSoup
import requests
import time


def str_to_list(some_str):
	'''
		Die einzelnen Zeichen der HTML Seite
		werden in eine einzelne Liste umgewandelt.
	'''
	list_str = []
	for c in range(0, len(prt)):
		list_str.append(prt[c])
	return list_str

def clean_list(liste):
	'''
		Alle Zeichen mit einem ASCII Wert
		über 256 werden ersetzt.
		Ohne diese Maßnahme können die Auswertungen
		nicht gespeichert werden.
	'''
	sauber_str = ''
	for zeichen in liste:
		if ord(zeichen) > 256:
			zeichen = '@'
		sauber_str += zeichen
	return sauber_str

base_url = 'https://www.ackerwaldundwiese.de/index.php?typ_or[]=Wald&land=Deutschland&action=searchresults&pclass[]=1&sortby=listingsdb_id&sorttype=DESC&cur_page='
seitennummer = 0

''' Erste Seite aufrufen '''
src = requests.get(base_url+str(seitennummer))

''' HTML auswerten '''
soup = BeautifulSoup(src.text, "html.parser")

''' Suche nach Anzahl Objekte eintrag '''
anzahl_obj = soup.find("span", class_="highlight")
''' und 10er Schritte ermitteln 
	weil die Seite immer 10 Einträge zeigt.
'''
anzahl = int(anzahl_obj.text)
steps = int(anzahl/10)
if anzahl/10.0 > steps:
	steps += 1

''' im logfile werden die Ergebnisse gespeichert '''
logfile = open('aww_data.csv', 'w')
print('Titel;Preis;Lage;Groesse')
''' Spaltennamen speichern '''
logfile.write('Titel;Preis;Lage;Groesse\n')
for step in range(steps):
	''' Fortschritt anzeigen '''
	print(f'Step: {step} of {steps}')
	''' Aufbau der URL, um die richtige Seite
		aufzurufen.
	'''
	src = requests.get(base_url+str(seitennummer))
	prt = src.text
	''' Diese Seite hat einige komisch formatierte
		Zeichen. Z.B. €
		Siehe die Kommentare zu den einelnen
		Funktionen (weiter oben).
	'''
	str_liste = str_to_list(prt)
	str_sauber = clean_list(str_liste)
	soup = BeautifulSoup(str_sauber, "html.parser")
	''' Die einzelnen Angeboten suchen '''
	objekte = soup.find_all("div", class_="object clearfix")
	for eintrag in objekte:
		''' Die einzelnen Elemente finden '''
		title = eintrag.find("div", class_="object-title")
		preis = eintrag.find("div", class_="object-price")
		preis = preis.text.replace('€','')
		lage = eintrag.find("div", class_="object-address")
		lage = lage.text.replace('Lage', '').strip()
		groesse = eintrag.find("div", class_="object-size")
		groesse = groesse.text.replace('Fläche','').strip()
		eintrag_zeile = f'{title.text.strip()};{preis.strip()};{lage.strip()};{groesse.strip()}\n'
		logfile.write(eintrag_zeile)
		''' Mit flush wird dei Datei gespeichert,
			auch ohne dass, das scraping abgeschlossen
			ist.
		'''
		logfile.flush()
		''' Fortschritt ausgeben '''
		print(eintrag_zeile)
	seitennummer += 1
logfile.close()