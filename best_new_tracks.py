from bs4 import BeautifulSoup
from time import strftime
import requests, os.path, os, webbrowser

output = '<!DOCTYPE html> '
for i in [ str(x) for x in range(1,6) ]:

    page = requests.get('http://pitchfork.com/reviews/best/tracks/' + i)
    html = page.text

    soup = BeautifulSoup(html, 'html5lib')
    editorials = soup.find_all(class_='editorial')

    for e in editorials:
        p = e.find_all('p')[-1]
        output += str(p) + '\n\n'

output = output.replace('//www.', 'https://www.')
output = output.replace('="//', '="https://')

current_date = strftime('%Y-%m-%d')
path = 'best_new_tracks_' + current_date + '.html'

with open(path, 'w') as f:
    f.write(output)

filename = os.path.normpath(os.path.join(os.getcwd(), path))
webbrowser.open('file://' + filename)
