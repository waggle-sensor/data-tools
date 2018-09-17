#!/usr/bin/env python3
from html.parser import HTMLParser
import requests
import sys


class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return

        try:
            link = dict(attrs)['href']
        except KeyError:
            return

        if link.endswith('complete.latest.tar'):
            print(link)


url = sys.argv[1]

r = requests.get(url)
assert r.status_code == 200

parser = LinkParser()
parser.feed(r.text)
