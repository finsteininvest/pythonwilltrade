'''
	bsp_inf_stock.py

	Programm um,
	US
	Bruttosozialprodukt,
	Inflationsrate und
	S&P 500
	zu vergleichen

	Benötigt die CSV Dateien, die durch
	die get_ Programme aus dem Internet gespeichert
	wurden.

	Maerz 2020

	https://finsteininvest.pythonanywhere.com/
'''

import pandas as pd
import matplotlib.pyplot as plt

sp500 = pd.read_csv('sp_500_yearly.csv')
gdp = pd.read_csv('us_gdp.csv')
infla = pd.read_csv('us_inflation.csv')

merged_df = pd.merge(gdp, infla, on='year')
merged_df = pd.merge(merged_df, sp500, on='year')
df_changes = merged_df[['year','gdp_growth', 'inflation_rate_yoy', 'ann_change']]
# Auskommentieren um den Plot der Veränderungen seit 1929 zu sehen
#df_changes.plot(x='year')
#plt.xticks(df_changes['year'], rotation=90)
#plt.show()


df_for_corr = merged_df[['gdp_growth', 'inflation_rate_yoy', 'ann_change']]
# Auskommentieren für die letzten 10 Jahre
#df_for_corr = df_for_corr[-10:]
# Auskommentieren für die letzten 5 Jahre
#df_for_corr = df_for_corr[-5:]
corr = df_for_corr.corr()
plt.set_cmap('RdYlGn')
plt.matshow(corr)
plt.xticks(range(len(df_for_corr.columns)), df_for_corr.columns)
plt.yticks(range(len(df_for_corr.columns)), df_for_corr.columns)
plt.colorbar()
plt.show()