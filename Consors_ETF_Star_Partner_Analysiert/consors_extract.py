'''
    consors_extract.py

    Programm, um aus einem Consors
    PDF Dokument ETF Informationen
    zu extrahieren.
    
    Januar 2020

    https://finsteininvest.pythonanywhere.com
    https://https://github.com/finsteininvest/pythonwilltrade/tree/master/Consors_ETF_Star_Partner_Analysiert
'''

from bs4 import BeautifulSoup
import argparse
import os
import re
import operator
import progress
import requests
import json
import pickle
import time

def pdf_to_list(pdf_datei):
    '''
        Convert a pdf file to a html file using pdfminer
        command line tool.
        From the html file text and values are extracted and
        place in a list that is sorted by y and x coordinates.    
    '''
    value_list = []

    os.system(f'python3 pdf2txt.py -c utf-8 -t html \"{pdf_datei}\" > temp.html')

    with open('temp.html', encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    elements = soup.find_all('div', style = re.compile('.*textbox.*'))

    for element in elements:
        attribute = element.attrs
        m = re.search('.*left:(.*?)px.*', str(attribute))
        x = m.group(1)
        m = re.search('.*top:(.*?)px.*', str(attribute))
        y = m.group(1)
        value_list.append([int(y),int(x),element.text.strip()])
        #print (f'{y};{x};{element.text.strip()}')

    sorted_value_list = sorted(value_list, key = operator.itemgetter(0, 1))
    os.remove('temp.html')

    return sorted_value_list


if __name__ == "__main__":
    # Create command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pdf_file', help='Name of PDF file', required = True)
    args = parser.parse_args()

    liste = pdf_to_list(args.pdf_file)
    isin_list = []
    etf_names = []
    hit = False
    # Extrahier die ISIN aus dem PDF Text
    for entry in liste:
        y, x, text = entry
        print(entry)
        # ISIN steht immer an x = 260
        # Und wir wollen den Eintrag 'ISIN' nicht ausgeben
        if x == 260 and 'ISIN' not in text:
            isin_list.append(text)
            hit = True
        if x == 437 and hit == True:
            etf_names.append(text)
            hit = False
    print(len(isin_list), len(etf_names))
    kombi = zip(isin_list, etf_names)
    kombi_set = set(kombi)
    for eintrag in kombi_set:
        isin, name = eintrag
        print(f'{isin};{name}')

    # Lade die Kurse für die ISIN Liste herunter.
    # Die Kurse werden pro ISIN abgespeichert.
    current_isin_count = 0
    max_isin = len(isin_list)
    print('Lade ETF Kurse:')
    for isin in isin_list:
        progress.print_progress(current_isin_count, max_isin)
        current_isin_count += 1
        etf_kurse = requests.get(f'https://de.extraetf.com/api-v2/chart/?isin={isin}&currency_id=2')
        parsed = json.loads(etf_kurse.text)
        results = parsed['results']
        for result, kurse in results.items():
            if result == 'trinav':
                print(f'Kurse für {isin} werden gespeichert')
                pickle.dump( kurse, open( f'{isin}.p', "wb" ) )
        time.sleep(5)







