# -*- coding: UTF-8 -*-
import os
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

__author__ = 'Webdeziner.se'

dataFolder = 'data/';

if not os.path.exists(dataFolder):
    os.makedirs(dataFolder)


stock_urls = [
    'https://www.avanza.se/aktier/om-aktien.html/5247/investor-b',
    'https://www.avanza.se/aktier/om-aktien.html/5369/kinnevik-b'
]


def make_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'lxml')


def crawl():
    """" Create new file """
    fileName = 'export-' + datetime.now().strftime('%Y-%m-%d %H.%M.%S')+'.csv'
    openFile = open(dataFolder + fileName, 'w+')
    csvFile = csv.writer(openFile, delimiter=',', quoting=csv.QUOTE_ALL)
    csvFile.writerow(['stock', 'last price', 'percent', 'change', 'url'])

    for stock in stock_urls:

        soup = make_soup(stock)
        info_bar = soup.find('div', {'id': 'surface'})
        info_bar_row = info_bar.find_all('div', 'row')[1]
        info_bar_list = info_bar_row.find('ul')

        name = info_bar_list.get('data-intrument_name')
        last_price = info_bar_list.find('span', 'lastPrice').text
        change_percent = info_bar_list.find('span', 'changePercent').text
        change = info_bar_list.find('span', 'change').text

        csvFile.writerow([name, last_price, change_percent, change, stock])


    openFile.close()


crawl()
