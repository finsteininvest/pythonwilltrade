'''
    readconsors.py

    Programm, um Consors Abrechnungsdokumente in einem
    Verzeichnis einzulesen und in einer JSON Datei
    abzulegen.

    finsteininvest.pythonanywhere.com
'''

import os
import consors2json
import json
from tinydb import TinyDB

if __name__ == '__main__':
    # All PDF Dateien finden und in 
    # JSON umwandeln 'lassen'.
    files = os.listdir('.')
    for fname in files:
        if '.pdf' in fname:
            print('\t%s' % fname)
            consors2json.convert2csv(fname, 5)
    with open("events.json", "r") as read_file:
        obj = json.load(read_file)
        pretty_json = json.dumps(obj, indent=4)
        print(pretty_json)

    # Ab hier CSV Ausgabe
    db = TinyDB('events.json')
    positions = db.all()
    header = True
    with open('events.csv','w') as outfile:
        for position in positions:
            if header == True:
                header = False
                header_items = position.keys()
                for header_item in header_items:
                    outfile.write(f'{header_item};')
                outfile.write('\n')
            items = position.values() 
            for item in items:
                outfile.write(f'{item};')
            outfile.write('\n')

