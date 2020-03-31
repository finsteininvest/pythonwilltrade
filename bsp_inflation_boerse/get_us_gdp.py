'''
	get_us_gdp.py

	Programm um die US BSP Daten
	von The Balance herunterzuladen

	März 2020

	https://finsteininvest.pythonanywhere.com/
'''

from bs4 import BeautifulSoup
import requests
import pandas as pd

resp = requests.get('https://www.thebalance.com/us-gdp-by-year-3305543')
soup = BeautifulSoup(resp.text, 'html.parser')
table = soup.find('table', {'class':'mntl-sc-block-table__table'})


years_list = []


for row in table.findAll('tr')[1:]:
    year = row.findAll('td')[0].text.strip()
    real_gdp = row.findAll('td')[2].text.strip()
    gdp_growth = row.findAll('td')[3].text.strip()
    gdp_growth = gdp_growth.replace('%','')
    events = row.findAll('td')[4].text.strip()
    
    years_list.append([year,real_gdp,gdp_growth,events])

members_df = pd.DataFrame.from_records(years_list, columns=['year','real_gdp','gdp_growth','events'])
members_df.to_csv('us_gdp.csv', index=False)