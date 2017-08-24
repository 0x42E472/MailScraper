#!/usr/bin/env python

import requests
import ssl
from bs4 import BeautifulSoup
import random
import sys


class ScrapeEmails():
    """testing"""
    
    def __init__(self):
        self.link = "put the link here"

    def check_href(self, content):
        self.placeholder = "test"
        self.check_links = content.find_all('a', href=True)

        for link in self.check_links:
            if "@" in link['href']:
                oh_hai =link['href'].split(':')
                yield oh_hai[1]

    def check_text(self, content):
        words = content.get_text().split()
        for word in words:
            if "@" in word:
                yield word

    def dedup(self, link, text):
        t = []
        s = []
        for i in link:
            t.append(i)
            for e in text:
                s.append(e)
        fuck = list(set(t) - set(s))
        result = t + list(fuck)
        return result


        
    def get_it(self):
        content = []
        r = requests.get(self.link)
        html_doc = r.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        link_emails = self.check_href(soup)
        text_emails = self.check_text(soup)
        herro = self.dedup(link_emails, text_emails)
        print herro

        sys.exit()

        toText.close()
        print("Saved: " + str(name) + ".txt")
    
        counter = 0
        if len(sys.argv) > 1:
            path = sys.argv[1] 
        else:
        
            path = input("Path or URL:\n")
    
        if (path[0:4] == "http"):
            get_it(path, counter)
if __name__ == "__main__":
    se = ScrapeEmails()
    t = se.get_it()
    print t
