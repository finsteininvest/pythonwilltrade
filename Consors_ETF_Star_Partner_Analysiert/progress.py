'''
    progress.py

    Hilfsprogramme
    a) Zur Fortschrittsanzeige bei längeren Operationen.
    b) Den Bildschirm löaschen
    c) Debug meldungen auszugeben

    Januar 2020
'''

import sys
import os

def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar

    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)

    Source: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    #sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    print('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix), end="\r")

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def clear_screen():
    '''
        Biuldschirm leeren
    '''
    osname = os.name
    if name == 'posix':
        os.system('clear')
    elif name == 'nt' or name == 'dos':
        os.system('cls')

def debug(str):
    '''Kleine Funktion, um
    Meldungen auszugeben.
    Allerdings, nur wenn im debug modus.
    '''
    if DEBUG:
        print(str)