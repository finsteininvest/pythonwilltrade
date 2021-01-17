'''
    dividend_screener.py

    Ein Programm, um alle Aktien
    zu finden, die Dividenden zahlen
    und die Dividendenrendite auszurechnen.


'''

import requests
import json
import pandas as pd
import argparse
from tabulate import tabulate

api_key = ''


def screen_dividend_payers(exchange):
    '''Function to get stocks from financialmodelingprep
       trading in the given exchenge that pay a dividend.
       Then calculate the dividend yield and sort them
       descending.
       Finally print them nicely formated as a table.

    '''

    url = f'https://financialmodelingprep.com/api/v3/stock-screener?dividendMoreThan=0.01&apikey={api_key}'
    #print(url)
    #quit()
    r = requests.get(url)
    json_data = json.loads(r.text)
    df_div_stocks = pd.DataFrame.from_dict(json_data)
    df_div_stocks['dividend_yield'] = df_div_stocks['lastAnnualDividend']/df_div_stocks['price']*100
    df_div_stocks = df_div_stocks.sort_values(by='dividend_yield',ascending = False)
    df_div_stocks = df_div_stocks[df_div_stocks.exchangeShortName == exchange]
    df_div_stocks['companyName'] = df_div_stocks['companyName'].str[:50]
    print(tabulate(df_div_stocks[['symbol','companyName','dividend_yield','lastAnnualDividend','price','beta','exchange']],headers = 'keys'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--exchange', required = False, help = 'Filter on exchange')
    args = parser.parse_args()
    screen_dividend_payers(args.exchange)