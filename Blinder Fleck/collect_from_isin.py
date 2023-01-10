'''
    Programm, um aus einer Liste von ISIN
    historische Werte zu ermitteln.
'''

from bs4 import BeautifulSoup
import requests
import argparse
import re
import time

def main(datei):
    with open(datei, 'r') as infile:
        isins = infile.readlines()
    for isin in isins:
        print(isin)
        response = requests.get(f'https://www.ariva.de/search/search.m?searchname={isin}')
        match = re.search(r'https://www.ariva.de/(.*)\?utp=1', response.url)
        response = requests.get(f'https://www.ariva.de/{match.group(1)}/kurse/historische-kurse?go=1&boerse_id=131')
        soup = BeautifulSoup(response.text, "html.parser")
        secu = soup.find(attrs={"name": "secu"})
        secu_value = secu.attrs['value']
        download_link = f'https://www.ariva.de/quote/historic/historic.csv?secu={secu_value}&boerse_id=131&clean_split=1&clean_payout=&clean_bezug=1&min_time=10.1.2022&max_time=10.1.2023&trenner=%3B&go=Download'
        response = requests.get(download_link)
        file = open(f'{isin}.csv', "wb")
        file.write(response.content)
        file.close()
        quit()
        time.sleep(5)
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = 'collect_from_py',
        description = 'Programm um historische Werte aus einer ISIN \
                       zu ermitteln.')
    parser.add_argument('-f', '--file', required = True, help = 'Name der Datei mit den ISIN')
    args = parser.parse_args()
    main(args.file)
