'''
    industry_pe.py

    Code to find average Price Earnings Ratio per
    industry.

    You need an API Key from https://financialmodelingprep.com/


    https://finsteininvest.pythonanywhere.com/
    Oktober 2020
'''

import requests
import pickle
import pandas as pd
import json
from tabulate import tabulate
import numpy as np

def collect_stocks(key):
    url = f'https://financialmodelingprep.com/api/v3/stock-screener?apikey={key}'
    r = requests.get(url)
    pickle.dump(r, open('stock_list.pickle', 'wb'))

def get_pe_ratio_per_stock_and_industry(key):
    r = pickle.load(open('stock_list.pickle', 'rb'))
    df_stock_list = pd.read_json(r.text)
    df_stock_list = df_stock_list[['symbol','price','industry']]
    p_e_stock_list = []
    for index, stock in df_stock_list.iterrows():
        symbol = stock['symbol']
        url = f'https://financialmodelingprep.com/api/v3/income-statement/{symbol}?apikey={key}&limit=1'
        r = requests.get(url)
        income_statement = pd.read_json(r.text)
        try:
            eps = income_statement[['eps']].values[0]
            industry = stock['industry']
            price = stock['price']
            print(symbol, price / eps[0], industry)
            p_e_stock_list.append([symbol, abs(price / eps[0]), industry])
        except:
            pass
    df_p_e_stocks = pd.DataFrame(p_e_stock_list, columns = ['symbol','peratio','industry'])
    df_p_e_stocks =  df_p_e_stocks.replace(np.inf, np.nan).dropna()
    df_pe_industry = df_p_e_stocks.groupby('industry').mean()
    df_pe_industry = df_pe_industry.sort_values('peratio')
    pickle.dump(df_pe_industry , open('df_pe_industry.pickle', 'wb'))
    print(tabulate(df_pe_industry))


if __name__ == '__main__':
    api_key = 'dein api key von https://financialmodelingprep.com/developer'
    collect_stocks(api_key)
    get_pe_ratio_per_stock_and_industry(api_key)
