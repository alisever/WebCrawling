from functools import reduce

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from random import randint
import pyexcel

headers = {"Accept-Language": "en-US,en;q=0.5"}

all_data = []
link = []
pages = np.arange(1, 32)

for page in pages:

    m_page = requests.get("https://www.karar.com/ara?key=fet%C3%B6&" + "page=" + str(page),
                          headers=headers)

    soup = BeautifulSoup(m_page.text, 'html.parser')
    for page_div in soup.find_all('div', {'class': 'search-result'}):
        for header in page_div.find_all('div', {'class': 'item'}):
            link_div = header.find('a', {'href': True})['href']
            link.append('https://www.karar.com' + str(link_div))
# print(link)

for content in link:
    each_link = requests.get(content, headers=headers)
    soup_1 = BeautifulSoup(each_link.text, 'html.parser')
    # print(soup_1)
    row_items = []
    for cont in soup_1.find_all('div', {'class': 'article-detail news-detail'}):
        title = cont.find('h1', {'class': 'content-title'}).text
        dates = cont.find('div', {'class': 'content-date'})
        date = dates.find('time', {'datetime': True})['datetime']
        txt = []

        if len(cont.find_all('div', {'class': 'text-content'})) > 2:
            for text_ in cont.find_all('div', {'class': 'text-content'}):
                txt.append(text_.text)

        else:
            texts = cont.find('div', {'class': 'text-content'})
            for text_ in texts.find_all('p'):
                txt.append(text_.text)

        try:
            txt[0:] = [reduce(lambda x, y: x + y, txt[0:])]

        except:
            continue

        row_items.append(content)
        row_items.append(title)
        row_items.append(date)
        row_items.append(txt[0])
        row_items.append('Haber')
        all_data.append(row_items)
pyexcel.save_as(array=all_data, sheet_name='haberler', dest_file_name="Karar.xlsx")
