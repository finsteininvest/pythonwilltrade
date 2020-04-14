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

plattform_renditen = 					[0.08,0.08]
plattform_ausfallwahrscheinlichkeiten = [0.07,0.07]
invest_je_plattform = 					[500,500]

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