from functools import reduce

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
pages = np.arange(1, 2)

for page in pages:

    m_page = requests.get("https://www.dirilispostasi.com/makale/7541492/prof-dr-osman-kose/yanginlar-tahrik-ve-teror",
                          headers=headers)

    soup = BeautifulSoup(m_page.text, 'html.parser')
    title = soup.find('h1', {'itemprop': 'headline'}).text
    dates = soup.find('div', {'class': 'post-kunye link-5 underline'})
    date = dates.find('time', {'class': 'tarih'}).text
    txt = []
    texts = soup.find('article', {'class': 'post-text word dark-1 em mb20 on-swipe-content'})
    for text_ in texts.find_all('p'):
        txt.append(text_.text)
    try:
        txt[0:] = [reduce(lambda x, y: x + y, txt[0:])]
    except:
        continue
    print(date)
    print(txt)
