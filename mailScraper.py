#!/usr/bin/env python
import requests
import ssl
from bs4 import BeautifulSoup
import random
import sys


class ScrapeEmails():
    """Practicing some programming."""
    
    def __init__(self):
        """TODO: Change name to domain name of url, change url to accept file or arg"""
        self.name = "test"
        self.link = ""

    def check_href(self, content):
        """Check for emails in links."""
        self.placeholder = "test"
        self.check_links = content.find_all('a', href=True)

        for link in self.check_links:
            if "@" in link['href']:
                oh_hai =link['href'].split(':')
                yield oh_hai[1]

    def check_text(self, content):
        """Check the html for emails."""
        words = content.get_text().split()
        for word in words:
            if "@" in word:
                yield word

    def dedup(self, link, text):
        """Dedup the emails from both sources."""
        t = []
        s = []
        for i in link:
            t.append(i)
            for e in text:
                s.append(e)
        email_list = list(set(t) - set(s))
        result = t + list(email_list)
        return result


        
    def get_it(self):
        """TODO: Separate this out to another function"""
        content = []
        r = requests.get(self.link)
        html_doc = r.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        link_emails = self.check_href(soup)
        text_emails = self.check_text(soup)
        the_goods = self.dedup(link_emails, text_emails)
        f = open(self.name,"w+")
        for i in the_goods:
            f.write("{0}\n".format(i))
        f.close()

if __name__ == "__main__":
    se = ScrapeEmails()
    t = se.get_it()
