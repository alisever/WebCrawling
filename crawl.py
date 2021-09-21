from functools import reduce
import re
import requests
from requests import get
from bs4 import BeautifulSoup
import numpy as np
from time import sleep
from random import randint
import pyexcel

headers = {"Accept-Language": "en-US,en;q=0.5", 'User-Agent': 'Mozilla/5.0'}

all_data = []
link = []
pages = np.arange(2, 3)

for page in pages:

    m_page = requests.get("https://www.dirilispostasi.com/ara?key=%2A%2A%2A%2A%2A%2A%2A%2Afet%C3%B6%2A%2A%2A%2A%2A%2A%2A%2A&" + "page=" + str(page),
                          headers=headers)

    soup = BeautifulSoup(m_page.text, 'html.parser')
    for page_div in soup.find_all('section', {'class': 'postblock c-mask-ratio crop t-arsiv'}):
        for header in page_div.find_all('h3', {'class': 'b'}):
            link_div = header.find('a', {'href': True})['href']
            link.append('https:' + str(link_div))
    print(page)

for content in link:
    print(content)
    each_link = requests.get(content, headers=headers)
    soup_1 = BeautifulSoup(each_link.text.decode('utf8'), 'html.parser')
    print(type(soup_1))
    row_items = []
    if 'haber' in str(content):
        for cont in soup_1.find_all('div', {'class': 'base con custom pt30 pt20-sm pt20-ms'}):
            title = cont.find('h1', {'itemprop': 'headline'}).text
            dates = cont.find('p', {'class': 'us'})
            date = dates.find('span', {'class': 'tarih'}).text
            txt = []
            texts = cont.find('div', {'class': 'post-text mb20 word em dark-1 tleft'})
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
    elif 'makale' in str(content):
        for cont in soup_1.find_all('div', {'class': 'base con custom pt30 pt25-sm'}):
            title = cont.find('h1', {'itemprop': 'headline'}).text
            dates = cont.find('div', {'class': 'post-kunye link-5 underline'})
            date = dates.find('time', {'class': 'tarih'}).text
            txt = []
            texts = cont.find('article', {'class': 'post-text word dark-1 em mb20 on-swipe-content'})
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
            row_items.append('Makale')
    all_data.append(row_items)
#print(all_data)
pyexcel.save_as(array=all_data, sheet_name='haberler', dest_file_name="Dirilis.xlsx")
