'''
	ana_file_aww.py

	Schritt 1 bei der Ermittlung der
	Waldpreise in Deutschland.

	Programm, um Preise und PLZ zu ermitteln. Nutzt
	die Datei aww_data.csv aus Schritt 1: scrape_aww.py

	Erzeugt die Datei: resultate_aww.csv
	
	Dezember 2018
	Aktualisiert Dezember 2019
'''

import csv
import numpy as np
import pandas as pd
import re

ppqm = []
with open('aww_data.csv', 'r') as infile:
	data = csv.DictReader(infile, delimiter = ';')
	for row in data:
		'''
			Der Preis muss umgewandelt werden,
			damit dieser nachher für eine Berechnung
			genutzt werden kann.
		'''
		preis = row['Preis'].replace('@','')
		preis = preis.replace('.', '')
		preis = preis.replace('?', '')
		'''
			Groesse muss gesäubert werden.
			Und dann in qm umgerechnet.
			Hier geht es um die Umrechnung von hektar.
		'''
		if 'ha' in row['Groesse']: 
			groesse = row['Groesse'].replace('ha','')
			groesse = groesse.replace(',', '.')
			groesse = groesse.replace('?', '')
			groesse = groesse.replace('ca.', '')
			groesse = groesse.replace('h', '')
			groesse = float(groesse) * 10000
		'''
			Groesse muss gesäubert werden.
			Und dann in qm umgerechnet.
			Hier geht es um die Umrechnung von qm.
		'''
		if 'm@' in row['Groesse']:
			groesse = row['Groesse'].replace('m@','')
			groesse = groesse.replace('.', '')
			groesse = groesse.replace(',', '.')
			groesse = groesse.replace('?', '')
			groesse = groesse.replace('ca', '')
		'''
			PLZ ermitteln
		'''
		plz_m = re.search('(^[0-9]{5})',row['Lage'])
		try:
			plz = plz_m.group(0)
		except:
			plz = ''
		'''
			Wir wollen nur die Einträge, wo der Preis > 0,
			oder nicht na vorkommt.
			Zusätzlich gibt es einige "Reizangebot" mit
			einem Preis unter 10€. Diese Angebote haben nichts
			mit der Realität zu tun.
			Die Resultate werden in einer Liste gespeichert.
		'''
		if len(preis) > 0 and not 'na' in preis and float(preis) > 10 and not '+' in str(groesse) and not '-' in str(groesse) and not 'und' in str(groesse):
			print(preis, groesse)
			ppqm.append([float(preis)/float(groesse), row['Titel'], plz])
'''
	Liste in ein Dataframe umwandeln.
	Damit können wir einfach die Quartile durch
	pandas errechnen lassen.
'''
df = pd.DataFrame.from_records(ppqm, columns=['PpQm','Titel','PLZ'])
print(df.describe())
''' Ergebnisse speichern '''
df.to_csv('resultate_aww.csv', sep = ';')
