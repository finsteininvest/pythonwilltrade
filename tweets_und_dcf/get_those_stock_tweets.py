'''
    get_those_stock_tweets.py

    Ein Programm, um Aktien "Besprechungen" in
    deiner Timeline zu finden.

    Für jedes Symbol wird der DCF, aktueller Preis und der
    Unterschied nach
    https://financialmodelingprep.com
    ermittelt.

    April 2020
'''

import tweepy
import re
import fmp

def get_those_stock_tweets():
    p = re.compile('(\\$.*?)\\W')

    consumer_key = 'API Key'
    consumer_secret = 'API secret key'
    access_token = 'Access token'
    access_secret = 'Access token secret'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    tweets = api.home_timeline(count=200)
    stock_tweets = []
    symbols = []
    unique_symbols = []
    for tweet in tweets:
        if '$' in tweet.text:
            stock_list = p.findall(tweet.text)
            stock_tweets.append([tweet.text, stock_list])
            for symbol in stock_list:
                symbols.append(symbol)
    unique_symbols = set(symbols)
    return(stock_tweets, unique_symbols)

if __name__ == "__main__":
    tweet_liste, unique_symbols = get_those_stock_tweets()
    for tweet, stock_list in tweet_liste:
        print(f'{tweet}')
        print(stock_list)
        print('')
 
    for symbol in unique_symbols:
        symbol = symbol.replace('$', '')
        try:
            dcf, price = fmp.get_dcf(symbol)
            delta = (float(dcf)/float(price)-1)*100
            print(f'{symbol}: DCF: {dcf:.2f} Price: {price:.2f} Delta: {delta:.2f}%')
        except:
            print(f'No DCF for {symbol}')