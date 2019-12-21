'''
	geocode.py

	Schritt 3 bei der Ermittlung der
	Waldpreise in Deutschland.

	Programm, um die geographichen Koordinaten
	der PLZ der Waldgangebote zu ermitteln. Es wird
	auch ein Kluster (von 0 bis 6) für die Preise/qm erzeugt.

	Nutzt die Datei: resultate_aww.csv
	Erzeugt die Datei: lagen_Aww.csv

	Dezember 2018
	Aktualisiert Dezember 2019
'''

import json
import requests
import csv

def get_lat_lon(osm_data):
	osm_data = json.loads(osm_data)
	lat = ''
	lon = ''
	for data in osm_data:
		if data['lat'] and lat == '':
			lat = data['lat']
		if data['lon'] and lon == '':
			lon = data['lon']
	return lat,lon

response = requests.get('https://nominatim.openstreetmap.org/search?country=Germany&postalcode=85609&format=json')

lage_file = open('lagen_aww.csv', 'w')
lage_file.write(f'PPQM;PLZ;LAT;LON;ART\n')
with open('resultate_aww.csv', 'r') as infile:
	data = csv.DictReader(infile, delimiter = ';')
	for row in data:
		plz = row['PLZ']
		ppqm = row['PpQm']
		query = f'https://nominatim.openstreetmap.org/search?country=Germany&postalcode={plz}&format=json'
		response = requests.get(query)
		lat,lon = get_lat_lon(response.text)
		print(f'{plz} {lat} {lon}')
		if len(lon) > 0 and len(plz) > 0:
			if float(ppqm) < 1:
				art = 'T0'
			elif float(ppqm) >= 1 and float(ppqm) < 2:
				art = 'T1'
			elif float(ppqm) >= 2 and float(ppqm) < 3:
				art = 'T2'
			elif float(ppqm) >= 3 and float(ppqm) < 4:
				art = 'T3'
			elif float(ppqm) >= 4 and float(ppqm) < 5:
				art = 'T4'
			elif float(ppqm) >= 6 and float(ppqm) < 7:
				art = 'T5'
			elif float(ppqm) >= 7:
				art = 'T6'
			lage_file.write(f'{ppqm};{plz};{lat};{lon};{art}\n')
			lage_file.flush()
lage_file.close()
