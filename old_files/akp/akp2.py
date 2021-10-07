from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from functools import reduce
from tqdm import tqdm
from datetime import datetime
import multiprocessing as mp
import time
import json

headers = {"Accept-Language": "en-US,en;q=0.5", 'User-Agent': 'Mozilla/5.0'}
links = []
all_data = []


def get_urls():
    with open('akp.json') as json_file:
        data = json.load(json_file)
    for i in data:
        links.append(i['link'])


def get_content(f_links):
    row_items = []
    each_link = requests.get(str(f_links), headers=headers)
    #time.sleep(5)
    soup = BeautifulSoup(each_link.text, 'html.parser')
    try:
        for cont in soup.find_all('div', {'class': 'content clearfix newsDetail'}):
            title = cont.find('h1').text
            dates = cont.find('span').text
            size = len(dates)
            date = dates[:size - 8]
            txt = []
            for texts in cont.find_all('p'):
                txt.append(texts.text)
            try:
                txt[0:] = [reduce(lambda x, y: x + y, txt[0:])]
            except:
                continue
            row_items.append(f_links)
            row_items.append(title)
            row_items.append(date)
            row_items.append(txt[0])
    except:
        pass
        #row_items.append('Haber')
    #all_data.append(row_items)
    return row_items


if __name__ == "__main__":
    get_urls()
    scraping_start_time = datetime.now()
    pool = mp.Pool(mp.cpu_count())
    result_list_tqdm = []
    for result in tqdm(pool.imap(func=get_content, iterable=links), total=len(links)):
        result_list_tqdm.append(result)
    df = pd.DataFrame(result_list_tqdm)
    df.to_excel('akp2.xlsx', index=False, header=False, engine='xlsxwriter')