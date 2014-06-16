from bs4 import BeautifulSoup
from tpb import TPB, CATEGORIES, ORDERS
from first import first
from docopt import docopt
from itertools import islice
import requests, os.path, os, webbrowser


t = TPB('https://thepiratebay.org') # create a TPB object with default domain


doc = '''
Usage:
  best_new_albums.py [ -a <num_torrents> ]

Options:
  -a                Automatically download the last <num_torrents> torrents.
'''

def get_bnm():

    i = 1
    while True:
        page = requests.get('http://pitchfork.com/reviews/best/albums/' + str(i))
        html = page.text

        soup = BeautifulSoup(html, 'html5lib')
        reviews = soup.find(id='main')
        info = reviews.find_all(class_='info')

        for item in info:

            artist = item.find('h1').text
            album = item.find('h2').text

            yield artist, album

        i += 1


if __name__ == '__main__':

    arguments = docopt(doc)

    if arguments['-a']:
        num_torrents = int(arguments['<num_torrents>'])
        bnm = islice(get_bnm(), num_torrents)
    else:
        bnm = get_bnm()

    for artist, album in bnm:

        print artist + ' - ' + album
        decision = raw_input('(y/n)? ')

        while decision not in ['y', 'n']:
            decision = raw_input('(y/n)? ')
        if decision == 'n':
            continue
        else:
            torrents = t.search(artist + ' ' + album).category(CATEGORIES.AUDIO.MUSIC).order(ORDERS.SEEDERS.DES)
            link = first(torrents).magnet_link
            webbrowser.open(link)
