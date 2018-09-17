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


for url in sys.argv[1:]:
    r = requests.get(url)

    if r.status_code != 200:
        print('warning: {} bad status code {}'.format(url, r.status_code), file=sys.stderr)
        continue

    parser = LinkParser()
    parser.feed(r.text)
