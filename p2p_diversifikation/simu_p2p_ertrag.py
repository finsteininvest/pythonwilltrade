'''
	simu_p2p_ertrag.py

	Programm, um mit einer Monte Carlo Simulation
	zu ermitteln welche Renditen bei einer
	erwarteten Ausfallwahrscheinlichkeit
	wahrscheinlich erreichbar sind.

	April 2020
'''
import random
import matplotlib.pyplot as plt

# Parameter für die Simulation
rendite = 0
ausfallwahrscheinlichkeiten = 1
plattform_größe = 2

# Ausfallwahrscheinlichkeit
sicher 				 = 1
fast_sicher          = 0.93
wahrscheinlich       = 0.75
gleichwahrscheinlich = 0.5
wahrscheinlich_nicht = 0.3
fast_sicher_nicht    = 0.07
unmöglich            = 0

# Groesse des Investments (in Kategorie)
S = 500
M = 1000
L = 5000

# Hier werden die Parameter je Plattform eingestellt
# Bsp. name_der_plattform = [rendite, ausfallw., groesse]
mintos = [0.17,fast_sicher_nicht,L]
bondora = [0.00,fast_sicher_nicht,S]
estateguru =[0.0923,fast_sicher_nicht,L]
linked_finance = [0.0856,fast_sicher_nicht,L]
robocash = [0.1716,wahrscheinlich_nicht,S]
wisefund = [0.1705,wahrscheinlich_nicht,S]

# Alle Plattformen zusammengefasst
plattform_renditen = 					[mintos[rendite],bondora[rendite],estateguru[rendite],linked_finance[rendite],robocash[rendite],wisefund[rendite]]
plattform_ausfallwahrscheinlichkeiten = [mintos[ausfallwahrscheinlichkeiten],bondora[ausfallwahrscheinlichkeiten],estateguru[ausfallwahrscheinlichkeiten],linked_finance[ausfallwahrscheinlichkeiten],robocash[ausfallwahrscheinlichkeiten],wisefund[ausfallwahrscheinlichkeiten]]
invest_je_plattform = 					[mintos[plattform_größe],bondora[plattform_größe],estateguru[plattform_größe],linked_finance[plattform_größe],robocash[plattform_größe],wisefund[plattform_größe]]

# Plausicheck

if (len(plattform_renditen) == len(invest_je_plattform) == len(plattform_ausfallwahrscheinlichkeiten)) == False:
	print('Anzahl Renditen, Ausfallwahrscheinlichkeiten, Invest ja Plattform nicht uniform')
	print('Programm abbruch')
	quit()


summe_aller_ertraege = []

for simstep in range(0,49999):
	summe_ertrag_plattform = 0
	for i, plattform in enumerate(plattform_ausfallwahrscheinlichkeiten):
		if random.random() <= plattform:
			# Plattform ausgefallen
			ertrag = -invest_je_plattform[i]
		else:
			ertrag = invest_je_plattform[i] * plattform_renditen[i]
		summe_ertrag_plattform += ertrag 
	summe_aller_ertraege.append(summe_ertrag_plattform)

plt.hist(summe_aller_ertraege, bins=10)
plt.show()