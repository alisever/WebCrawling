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
pages = np.arange(1, 590)

for page in pages:

    m_page = requests.get("https://www.turkiyegazetesi.com.tr/arama?q=fet%C3%B6&" + "pg=" + str(page),
                          headers=headers)

    soup = BeautifulSoup(m_page.text, 'html.parser')
    for page_div in soup.find_all('div', {'class': 'category_other_list'}):
        for header in page_div.find_all('div', {'class': 'cat_item clearfix'}):
            link_div = header.find('a', {'href': True})['href']
            link.append(str(link_div))
# print(link)

for content in link:
    each_link = requests.get(content, headers=headers)
    soup_1 = BeautifulSoup(each_link.text.encode('ISO-8859-1').decode('utf8'), 'html.parser')
    row_items = []
    for cont in soup_1.find_all('div', {'class': 'news-container'}):
        try:
            title = cont.find('h1', {'class': 'page_title'}).text
            dates = cont.find('div', {'class': 'story_date clearfix'}).text
        except:
            continue
        txt = []

        texts = cont.find('div', {'class': 'article-body'})
        for text_ in texts.find_all('p'):
            txt.append(text_.text)
        # print(txt)
        last = []
        sub = '\n\n\n\n\n'
        for i in range(len(txt)):
            clear_text = txt[i].split(sub, 1)[0]
            last.append(clear_text)
            try:
                last[0:] = [reduce(lambda x, y: x + y, last[0:])]

            except:
                continue
        # print(last)
        row_items.append(content)
        row_items.append(title)
        row_items.append(dates)
        try:
            row_items.append(last[0])
        except:
            continue
        row_items.append('Haber')
        all_data.append(row_items)

pyexcel.save_as(array=all_data, sheet_name='haberler', dest_file_name="Turkiyegzt.xlsx")
