import requests
from bs4 import BeautifulSoup
import pandas as pd

start_url = 'https://www.sozcu.com.tr/'

sitemaps = ['https://www.sozcu.com.tr/tools/sitemaps/xml/sitemap_index.xml',
            'https://www.sozcu.com.tr/tools/sitemaps/xml/sitemap_sozcutv_index.xml',
            'https://www.sozcu.com.tr/sitemap_google_news.xml']


def sitemap_urls():
    while sitemaps:
        print(len(sitemaps))
        sitemap = sitemaps.pop()
        r = requests.get(sitemap)
        soup = BeautifulSoup(r.text, 'lxml')
        for loc in soup.find_all('loc'):
            if loc.string.endswith('.xml'):
                sitemaps.append(loc.string)
            else:
                with open('sozcu_sitemap.csv', 'a') as fd:
                    fd.write(loc.string + '\n')


if __name__ == '__main__':
    data = pd.read_csv('sozcu_sitemap.csv')
