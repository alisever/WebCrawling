from functools import reduce

import requests
from requests import get
from bs4 import BeautifulSoup
import numpy as np
from time import sleep
from random import randint
import pyexcel

headers = {"Accept-Language": "en-US,en;q=0.5"}

all_data = []
link = []
pages = np.arange(1, 667)

for page in pages:

    m_page = requests.get("https://www.internethaber.com/arama?key=fet%C3%B6&" + "page=" + str(page),
                          headers=headers)

    soup = BeautifulSoup(m_page.text, 'html.parser')
    for page_div in soup.find_all('div', {'class': 'col-12 col-lg mw0'}):
        for header in page_div.find_all('div', {'class': 'news-list left-image left-image-big mb-md'}):
            link_div = header.find('a', {'href': True})['href']
            link.append(str(link_div))
    print(page)

for content in link:
    each_link = requests.get(content, headers=headers)
    soup_1 = BeautifulSoup(each_link.text, 'html.parser')
    row_items = []
    for cont in soup_1.find_all('div', {'class': 'news-detail'}):
        try:
            title = cont.find('h1', {'class': 'news-detail__title'}).text
            dates = cont.find('div', {'class': 'ml-auto'})
            date = dates.find('time', {'datetime': True}).text
            #print(date)

        except:
            continue
        txt = []
        texts = cont.find('div', {'class': 'content-text'})
        for text_ in texts.find_all('p'):
            txt.append(text_.text)
        try:
            txt[0:] = [reduce(lambda x, y: x + y, txt[0:])]

        except:
            continue
        row_items.append(content)
        row_items.append(title)
        row_items.append(date)
        try:
            row_items.append(txt[0])
        except:
            continue
        row_items.append('Haber')
        all_data.append(row_items)
pyexcel.save_as(array=all_data, sheet_name='haberler', dest_file_name="Internethaber.xlsx")
