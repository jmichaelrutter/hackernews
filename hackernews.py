"""
hackernews.py

Creates a connection to news.ycombinator.com and scrapes the titles
and links from the front page.  Output is a tidy table replicating
the page.
"""

import requests
from tabulate import tabulate
from bs4 import BeautifulSoup

# Establish webpage connection
try:
    page = requests.get("https://news.ycombinator.com/news?p=1")
except requests.exceptions.ConnectionError:
    print("No network connection to provided URL. Check connectivity and URL name.")
    exit()

# Ensure response from server is good
if page.status_code == 200:

    soup = BeautifulSoup(page.content, 'html.parser')   # Scrape webpage HTML data
    table = list()

    # Iterate over the 'a' tags in the HTML data that are of class 'titlelink'
    # These are the tags that contain desired payload
    for i, item in enumerate(soup.find_all('a', class_='titlelink')):
        entry = list()
        entry.append('[' + str(i+1) + ']')  # Entry number
        entry.append(item.get_text())       # Entry title
        # Links to posts on the host do not include the full URL, so this
        # check ensures a fully qualified URL is included
        if item['href'][0:4] == 'item':
            item['href'] = 'https://news.ycombinator.com/' + item['href']
        entry.append(item['href'])          # Entry link
        table.append(entry)

    # Output result
    print(tabulate(table, headers=['No.', 'Title', 'Link']))

else:
    print("Connection refused")
