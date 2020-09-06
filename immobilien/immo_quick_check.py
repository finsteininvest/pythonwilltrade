'''
	immo_quick_check.py

	Programm, um ein Gefühl zu bekommen,
	ob ich eine Immobilie kaufen
	soll, oder  nicht.


	August 2020

	https://finsteininvest.pythonanywhere.com/
'''

import argparse
import numpy as np
from numpy import arange

def check_monthly_payments(zins, kreditbetrag, laufzeit):
	'''Berechnet die Annuität.

	Berechnet die monatliche Annuität,
	bei der Voragabe von:
	- Kreditbetrag,
	- anfänglichen Zins,
	- Laufzeit des Kredits
	'''

	monthlyPayment = np.pmt(zins/12, \
		             laufzeit, kreditbetrag);

	zins = zins * 100
	laufzeit = laufzeit/12
	print('Welche Annuität bei gegebenen:')
	print('Zins, Laufzeit und Kreditbetrag?')
	print(f'Kreditbetrag: {kreditbetrag}')
	print(f'Zins: {zins}%')
	print(f'Laufzeit in Jahren: {laufzeit}')
	print(f'Monatliche Annuität (Zins+Rückzahlung): {monthlyPayment:0.2f}')
	yearlyPayment = monthlyPayment * 12
	print(f'Jährliche Annuität (Zins+Rückzahlung): {yearlyPayment:0.2f}')

def check_monthly_annuity_on_amount(laufzeit, zins, kredit_start, kredit_ende, schrittweite):
	'''Berechnet Annuität bei ändernden Kreditbetrag

	'''

	print('Wie verändert sich meine Annuität')
	print('bei verändertem Kreditbetrag?')
	laufzeit_jahre = laufzeit/12
	print(f'Laufzeit in Jahren: {laufzeit_jahre}')
	zins_in_prozent = zins * 100
	print(f'Zins: {zins_in_prozent:0.2f}%')

	for kreditbetrag in arange(kredit_start, kredit_ende+schrittweite, schrittweite):
		monthlyPayment = np.pmt(zins/12, \
			             laufzeit, kreditbetrag);
		zins_in_prozent = zins * 100
		laufzeit_in_Monaten = laufzeit/12
		print(f'Kreditbetrag: {kreditbetrag}')
		print(f'Monatliche Annuität (Zins+Rückzahlung): {monthlyPayment:0.2f}')
		yearlyPayment = monthlyPayment * 12
		print(f'Jährliche Annuität (Zins+Rückzahlung): {yearlyPayment:0.2f}')

def check_monthly_annuity(kreditbetrag, laufzeit, zins_start, zins_ende, step):
	'''Berechnet Annuität bei veränderten Zinsen

	'''

	print('Wie verändert sich meine Annuität')
	print('bei verändertem Zins?')
	print(f'Kreditbetrag: {kreditbetrag}')
	laufzeit_jahre = laufzeit/12
	print(f'Laufzeit in Jahren: {laufzeit_jahre}')


	for zins in arange(zins_start, zins_ende, step):
		monthlyPayment = np.pmt(zins/12, \
			             laufzeit, kreditbetrag);
		zins_in_prozent = zins * 100
		laufzeit_in_Monaten = laufzeit/12
		print(f'Zins: {zins_in_prozent:0.2f}%')
		print(f'Monatliche Annuität (Zins+Rückzahlung): {monthlyPayment:0.2f}')
		yearlyPayment = monthlyPayment * 12
		print(f'Jährliche Annuität (Zins+Rückzahlung): {yearlyPayment:0.2f}')

def check_zins_betrag(laufzeit, \
			          kredit_start, kredit_ende, schrittweite, \
					  zins_start, zins_ende, zins_step):
    '''Berechnet Annuität bei sich ändernden Zins und Kreditbetrag

    '''

	zins_reihe = ['Betrag']
	for zins in arange(zins_start, zins_ende, zins_step):
		zins_in_prozent = zins*100
		zins_reihe.append(f'{zins_in_prozent:.2}')
	zins_reihe = [zins.replace('.',',') for zins in zins_reihe]
	print(';'.join(zins_reihe))

	zins_reihe = []
	for kreditbetrag in arange(kredit_start, kredit_ende+schrittweite, schrittweite):
		zins_reihe.append(str(kreditbetrag))
		for zins in arange(zins_start, zins_ende, zins_step):
			monthlyPayment = np.pmt(zins/12, \
			             laufzeit, kreditbetrag);
			zins_reihe.append(f'{monthlyPayment:.2f}')
		zins_reihe = [zins.replace('.',',') for zins in zins_reihe]
		print(';'.join(zins_reihe))
		zins_reihe = []

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-k','--kreditbetrag', help ='Kreditbetrag') 
	parser.add_argument('-z','--zins', help = 'Jährlicher Zins')
	parser.add_argument('-l', '--laufzeit', help = 'Laufzeit in Monaten')
	parser.add_argument('-t', '--kalkulationsart', required=True, help = 'Kalulationsart: [annuität,]')
	args = parser.parse_args()

	if args.kalkulationsart == 'tilgung':
		check_monthly_payments(float(args.zins), float(args.kreditbetrag), float(args.laufzeit))
	if args.kalkulationsart == 'annuität':
		zins_start, zins_ende, step = args.zins.split(':')
		check_monthly_annuity(float(args.kreditbetrag), float(args.laufzeit), float(zins_start), float(zins_ende), float(step))
	if args.kalkulationsart == 'kredit':
		kredit_start, kredit_ende, schrittweite = args.kreditbetrag.split(':')
		check_monthly_annuity_on_amount(float(args.laufzeit), float(args.zins), float(kredit_start), float(kredit_ende), float(schrittweite))
	if args.kalkulationsart == 'zinsbetrag':
		zins_start, zins_ende, zins_step = args.zins.split(':')
		kredit_start, kredit_ende, schrittweite = args.kreditbetrag.split(':')
		check_zins_betrag(float(args.laufzeit), \
			              float(kredit_start), float(kredit_ende), float(schrittweite), \
						  float(zins_start), float(zins_ende), float(zins_step))