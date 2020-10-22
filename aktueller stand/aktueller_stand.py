'''
    aktueller_stand.py

    Program to extract Stock Market indexes
    from a web site

    December, 2018
'''



# Use requests to grab the web page
import requests

# Use BeautifulSoup to parse the html of the web page
from bs4 import BeautifulSoup

# Use pickle to store results
import pickle

# Use to check if pickle file exists
import os

# Use to clear screen
from subprocess import call

# Use to print colored output
from colorama import init, Fore, Back, Style

# Use to loop
import time


def get_and_display():
    # Grab index information from Onvista
    r = requests.get('https://www.onvista.de/index/')
    html_doc = r.text
    # and parse the html
    soup = BeautifulSoup(html_doc, 'html.parser')
    # use trigger to toggle output
    trigger_counter = 0
    
    data = []
    # go through all table data html
    for td in soup.find_all('td'):
        # get all class entries
        cl = td.get('class')
        # each index is contained in a reference html tag
        refs = td.find_all('a')
        try:
            if trigger_counter == 2:
                trigger_counter = 0            
                # Index entry found.
                # Now get current value from table cell data
                
                wert = td.text.rjust(15," ")
                # Convert to something that is recognized as a value
                wert = wert.replace('.','')
                wert = wert.replace(',','.')
                # Store symbol and value
                data.append([txt.strip(),wert.strip()])
            if trigger_counter == 1:
                # trigger_counter used to get the second cell
                # after index row find
                trigger_counter += 1
            if 'TEXT' in cl:
                # if class is of type TEXT
                # check if the text in html tag
                # contains one the indexes in question
                for ref in refs:
                    txt = ref.text
                    if txt in ['DAX', 'MDAX','SDAX','TecDAX', 'Dow Jones','S&P 500','NASDAQ 100', 'Nikkei 225', 'Hang Seng']:
                        # found one of the indexes in question to output
                        txt = txt.ljust(10," ")
                        trigger_counter = 1
        except:
            continue
    
    # Check if previous data is available
    if os.path.isfile('./last.p'):
        last_list = pickle.load( open( "last.p", "rb" ) )
    
        # loop through current and previous data
        # to match symbols and compare values
        for symbol,val in data:
            for last_symbol,last_val in last_list:
                if symbol == last_symbol:
                    # Check and mark direction of movement
                    if float(val) > float(last_val):
                        direction = "/"
                        print(Back.GREEN + f'{symbol.ljust(10," ")}{val.rjust(15," ")}{direction}')
                    if float(val) < float(last_val):
                        direction = "\\"
                        print(Back.RED + f'{symbol.ljust(10," ")}{val.rjust(15," ")}{direction}')
                    if float(val) == float(last_val):
                        direction = "-"
                        print(f'{symbol.ljust(10," ")}{val.rjust(15," ")}{direction}')
            
    # No previous data available
    else:
        for symbol,val in data:
            print(f'{symbol.ljust(10," ")}{val.rjust(15," ")}')
        
    print('\n\n\n')
    
    # Store data
    pickle.dump( data, open( "last.p", "wb" ) )

if __name__ == '__main__':
    while True:
        call('clear' if os.name =='posix' else 'cls')
        init()
        get_and_display()
        # Repeat every 10 minutes
        time.sleep(60*10)
