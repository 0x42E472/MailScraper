#!/usr/bin/env python

import re
import sys
import argparse
import requests
import Queue
import threading
import yaml
import time
import traceback
from colorama import Fore, Style, init

#
# TODO: This probably needs more error handling....maybe
# TODO: The default config shouldn't be the URLS.yml test config
#


#
# Class that scrapes a URL and find all the email addresses on the page
# 
class ScrapeEmails():

    def __init__(self, timeout=30):
        self.timeout = timeout
        self.email_regex = re.compile(r"([a-zA-Z0-9._%-]+@[a-zA-Z-9._%-]+\.[a-zA-Z]{2,6})")

    def _get(self, url):
        return requests.get(url, timeout=self.timeout, verify=True)

    def scrape(self, url):
        emails = []
        response = self._get(url)

        if response.status_code == 200:
            emails = self.email_regex.findall(response.text)

        return emails

#
# This is the worker, it calls the scrapper calss when it has work
#
class ThreadWorker(threading.Thread):

    def __init__(self, thread_id, name, queue, lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.queue = queue
        self.lock = lock
        self.scrapper = ScrapeEmails()

    def run(self):
        print "Starting {0}".format(self.name)

        while not self.queue.empty():
            self.lock.acquire()

            if not self.queue.empty():
                url = self.queue.get()
                self.lock.release()

                emails = self.scrapper.scrape(url)

                if len(emails) > 0:
                    for email in emails:
                        print(Fore.GREEN + "{0}: {1} -- Found: [{2}]" \
                              .format(self.name, url, email))
                else:
                    print(Fore.RED + "{0}: {1} -- No emails Found" \
                          .format(self.name, url))

            else:
                self.lock.release()

            time.sleep(1)

        print(Fore.YELLOW + "Stopping {0}".format(self.name))


#
# Method to load a config yaml file
#
def load_yaml_config(filename):
    data = None

    with open(filename, 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as e:
            ValueError(e)

    return data


#
# Closes all the threads
#
def close_all_threads(queue_lock, threads):
    queue_lock.acquire()

    queue = None

    # Stop all threads
    for t in threads:
        t.join()

    queue_lock.release()


#
# Fills the queue with URLs
#
def fill_queue(queue,lock,urls):
    lock.acquire()
    for url in urls:
        queue.put(url)
    lock.release()


#
# Parses command line arguments
#
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default='URLS.yml', help='Yaml config file containing the URLs')
    parser.add_argument('-T', '--timeout', default=30, help='Seconds to wait for a URL response')
    parser.add_argument('-t', '--threads', default=1, help='Number of threads to create')

    # Show usage if wedon't have what we need
    if 'file' not in parser.parse_args():
        parser.print_help()

    return parser.parse_args()


#
# Main - Puts it all together
#
def main():
    init(autoreset=True)
    # Get command line args
    args = parse_args()

    # Setup things that we need
    lock = threading.Lock()
    queue = Queue.Queue()
    threads = []
    stop_threads = False

    # Load config file
    config = load_yaml_config(args.file)

    # fill the queue
    fill_queue(queue, lock, config['urls'])

    # Create the threads
    for thread_id in range(1, int(args.threads) + 1):
        name = "Thread-{0}".format(thread_id)
        thread = ThreadWorker(thread_id, name, queue, lock)
        thread.start()
        threads.append(thread)

    # Wait for the queue to empty
    while not queue.empty():
        pass

    # Stop all threads
    close_all_threads(lock, threads)

    print 'Exiting Main'
    sys.exit(0)


#
# Only run main() if this file was executed directly  
#
if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
