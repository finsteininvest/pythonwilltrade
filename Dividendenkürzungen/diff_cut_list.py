'''
	diff_cut_list.py

	Programm um Dividendenaristokraten
	zu finden, die ihre Dividende gekürzt
	haben.

	Mai 2020
	https://finsteininvest.pythonanywhere.com
'''
import argparse

def abgleich(cut_list, aristokraten_liste):
	for symbol in aristokraten_liste:
		if symbol in cut_list:
			print(symbol)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--cutlist', help='Datei der Cutliste', required=True)
	parser.add_argument('-a', '--aristokratlist', help='Datei der Aristokraten', required=True)
	args = parser.parse_args()
	cutlist = []
	aristokratlist = []

	with open(args.cutlist) as cutlistfile:
		cutlistitems = cutlistfile.readlines()
		for item in cutlistitems:
			name, symbol = item.split(';')
			symbol = symbol.strip()
			cutlist.append(symbol)

	with open(args.aristokratlist) as aristokratfile:
		aristokratlistitems = aristokratfile.readlines()
		for item in aristokratlistitems:
			items = item.split(',')
			symbol = items[0].replace('"','')
			aristokratlist.append(symbol)

	#print(aristokratlist)
	#print(cutlist)
	abgleich(cutlist, aristokratlist)