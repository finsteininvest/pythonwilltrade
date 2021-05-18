'''
    consors2json.py

    Programm, um PDF Dokumente
    der Consors Bank auszulesen und
    bestimmte Inhalte
    als JSON Datenbank abzuspeichern.

    Erkannte Dokumente:
    - Verkaufsabrechnung
    - Kaufabrechnung
    - Ertragsgutschriften
    - Dividendengutschriften

    finsteininvest.pythonanywhere.com

'''

import argparse
import os
from bs4 import BeautifulSoup
import re
import operator
from tinydb import TinyDB,Query

def pdf_to_list(pdf_file):
    ''' Convert a pdf file to a html file using pdfminer
        command line tool.
        From the html file text and values are extracted and
        place in a list that is sorted by y and x coordinates.

    '''
    
    value_list = []

    os.system(f'python3 pdf2txt.py -c utf-8 -t html \"{pdf_file}\" > temp.html')

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


    sorted_value_list = sorted(value_list, key = operator.itemgetter(0))
    os.remove('temp.html')

    return sorted_value_list

def cluster_list(data, maxgap):
    '''Arrange data into groups where successive elements
       differ by no more than *maxgap*

        >>> cluster([1, 6, 9, 100, 102, 105, 109, 134, 139], maxgap=10)
        [[1, 6, 9], [100, 102, 105, 109], [134, 139]]

        >>> cluster([1, 6, 9, 99, 100, 102, 105, 134, 139, 141], maxgap=10)
        [[1, 6, 9], [99, 100, 102, 105], [134, 139, 141]]

        Source:
        https://stackoverflow.com/questions/14783947/grouping-clustering-numbers-in-python#14783980

    '''

    data.sort()
    groups = [[data[0]]]
    for x in data[1:]:
        if abs(x - groups[-1][-1]) <= maxgap:
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups

def get_group_members(list, group):
    '''Function to find all text that belongs together
       based on their y value belonging to a group

    '''

    group_members = []
    last_list_item = 0
    for item in group:
        for index, list_item in enumerate(list):
            if index >= last_list_item:
                if item == list_item[0]:
                    group_members.append(list_item)
                    last_list_item = index+1
                    break
    sorted_group_members = sorted(group_members, key = operator.itemgetter(1))
    return sorted_group_members

def identify_document_type(group_members_list):
    '''Function to identify the document type
       from a list of text.
       Returns the document type as a string
      
    '''

    doc_type = ''
    for group in group_members_list:
        for item in group:
            #print(item)
            if 'VERKAUF' == item[2]:
                doc_type = 'VERKAUF'
            if 'KAUF' == item[2]:
                doc_type = 'KAUF'
            if 'Dividendengutschrift' == item[2]:
                doc_type = 'Dividendengutschrift'
            if 'Ertragsgutschrift' == item[2]:
                doc_type = 'Ertragsgutschrift'

    return doc_type

def collect_data(group_members_list):
    wkn = ''
    isin = ''
    stueck = ''
    kurs = ''
    kurswert = ''
    provision = ''
    gebuehr = ''
    datum = ''
    bezeichnung = ''
    get_kurs = False
    nettowert = ''
    get_kurswert = -1
    get_netto = -1
    for group in group_members_list:
        for item in group:
            if get_kurswert == 0:
                get_kurswert = -1
                werte = item[2]
                werteliste = werte.split('\n')
                kurswert = werteliste[0]
                try:
                    provision = werteliste[1]
                except:
                    pass
                try:
                    gebuehr = werteliste[2]
                except:
                    pass
            if 'Bezeichnung' in item[2]:
               bez_liste = item[2].split('\n')
               bezeichnung = bez_liste[1]
            if get_netto == 0:
                nettowert = item[2]
                get_netto = -1
            if get_kurswert > 0:
                get_kurswert = get_kurswert - 1
            if get_netto > 0:
                get_netto = get_netto - 1
            if get_kurs == True:
                get_kurs = False
                kurs = item[2]
                kurs = kurs.replace(' EUR P.ST.', '')
            if 'AM' in item[2]:
                datum = item[2]
                datum = datum.replace('AM ', '')
                datum = datum[0:10]
            if 'Umsatz' in item[2]:
                stueck = item[2].replace('\n', ' ')
                stueck = stueck.replace('Umsatz ', '')
            if 'WKN' in item[2]:
                wkn = item[2].replace('\n', ' ')
                wkn = wkn.replace('WKN ', '')
            if 'ISIN' in item[2]:
                isin = item[2].replace('\n', ' ')
                isin = isin.replace('ISIN ', '')
            if 'Kurs' == item[2]:
                get_kurs = True
            if 'Kurswert' in item[2]:
                get_kurswert = 1
            if 'Netto zugunsten' in item[2]:
                get_netto = 1

    return bezeichnung, wkn,isin,stueck,kurs,kurswert,provision,gebuehr,datum,nettowert


def convert2csv(pdf_file, maxgap):
    '''Workhorse function to convert a pdf file
       and store extracted contents in a json file.

    '''

    list = pdf_to_list(pdf_file)
    y_data = []
    for y,x,text in list:
        y_data.append(y)
    groups = cluster_list(y_data, maxgap)
    year = '-'
    group_members_list = []
    for group in groups:
        group_members = get_group_members(list, group)
        group_members_list.append(group_members)
        line = ''
        
    doc_type = identify_document_type(group_members_list)
    print(doc_type)
    bezeichnung,wkn,isin,stueck,kurs,kurswert,provision,gebuehr,datum, nettowert = collect_data(group_members_list)
    print(bezeichnung,wkn,isin,stueck,kurs,kurswert,provision,gebuehr,datum,nettowert)
    db = TinyDB('events.json')
    db.insert({'event_type':doc_type, 
        'bezeichnung':bezeichnung,
        'wkn':wkn,
        'isin':isin,
        'stueck':stueck,
        'kurs':kurs,
        'kurswert':kurswert,
        'provision':provision,
        'gebuehr':gebuehr,
        'datum':datum,
        'nettowert':nettowert,
        'reference':pdf_file})

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='PDF file to convert', required = True)
    args = parser.parse_args()

    list = convert2csv(args.file, maxgap=5)
