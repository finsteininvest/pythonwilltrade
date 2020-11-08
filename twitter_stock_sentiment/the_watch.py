'''
    the_watch.py

    A program to get sentiments
    on a stock

    September 2020
    https://finsteininvest.pythonanywhere.com

    Inspiriert durch: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
'''


import tweepy
import re
# This file contains the Twitter
# credentials
import conf
from textblob import TextBlob
import argparse

def print_logo(symbol):
    '''Stupid utility function to print
       the logo of this program

    '''

    print(f'The        |              Symbol: {symbol}')
    print('Watch     /#\\')
    print('          |o|-------------=================')
    print('         /###\\')
    print('         |###|')
    print('         |###|')
    print('        |#####|')
    print('        |#####|')
    print(' ______/#######|')
    print('/##############|')
    print('|##############|')
    print('|##############|')
    print('----------------')

def clean_tweet(tweet):
    '''Utility function to clean tweet text by removing links, special characters
       using simple regex statements.

    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''Utility function to get the sentiment
       of a single tweet.

    '''

    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def collect_sentiment(symbol):
    '''Fetch all tweets for a symbol
       and get the sentiment for each
       tweet.

    '''

    auth = tweepy.OAuthHandler(conf.consumer_key, conf.consumer_secret)
    auth.set_access_token(conf.access_token, conf.access_secret)
    api = tweepy.API(auth)
    symbol = f'${symbol} '
    tweets = []
    fetched_tweets = api.search(q = symbol, count = 1000)
    for tweet in fetched_tweets:
        # empty dictionary to store required params of a tweet
        parsed_tweet = {}
        # saving text of tweet
        parsed_tweet['text'] = tweet.text
        # saving sentiment of tweet
        parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)
        # appending parsed tweet to tweets list
        if tweet.retweet_count > 0:
            # if tweet has retweets, ensure that it is appended only once
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
            tweets.append(parsed_tweet)
    # return parsed tweets
    positive = 0
    neutral = 0
    negative = 0
    for tweet in tweets:
        print(tweet['text'])
        print(tweet['sentiment'])
        print('-----------------------------------')
        if 'positive' in tweet['sentiment']:
            positive += 1
        if 'negative' in tweet['sentiment']:
            negative += 1
        if 'neutral' in tweet['sentiment']:
            neutral += 1
    return positive,neutral,negative


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--symbol', help ='Symbol for sentiment check.', required = True)
    args = parser.parse_args()

    pos,neut,neg = collect_sentiment(args.symbol)
    print_logo(args.symbol)
    print(f'Positive: {pos}')
    print(f'Neutral: {neut}')
    print(f'Negative: {neg}')
    print(f'Ratio: {pos/neg}')
