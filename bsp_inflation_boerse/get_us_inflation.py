'''
	get_us_inflation.py

	Programm um due US Inflationsdaten
	von The Balance herunterzuladen

	März 2020

	https://finsteininvest.pythonanywhere.com/
'''

from bs4 import BeautifulSoup
import requests
import pandas as pd

resp = requests.get('https://www.thebalance.com/u-s-inflation-rate-history-by-year-and-forecast-3306093')
soup = BeautifulSoup(resp.text, 'html.parser')
table = soup.find('table', {'class':'mntl-sc-block-table__table'})


years_list = []


for row in table.findAll('tr')[1:]:
    year = row.findAll('td')[0].text.strip()
    inflation_rate_yoy = row.findAll('td')[1].text.strip()
    inflation_rate_yoy = inflation_rate_yoy.replace('%','')
    bus_cycle = row.findAll('td')[3].text.strip()
    events = row.findAll('td')[4].text.strip()
    
    years_list.append([year,inflation_rate_yoy,bus_cycle,events])

members_df = pd.DataFrame.from_records(years_list, columns=['year','inflation_rate_yoy','bus_cycle','events'])
members_df.to_csv('us_inflation.csv', index=False)