import json
import requests
import random

from bs4 import BeautifulSoup

# with open('agents.txt', 'r') as f:
#     agents = [line.rstrip() for line in f.readlines()]
#
# base = 'https://www.dirilispostasi.com/ara?key=fet%C3%B6&page={}'
#
# start_urls = [base.format(i) for i in range(1, 752)]
#
# all_list = []
# for index, link in enumerate(start_urls):
#     if index % 10 == 0:
#         print(index)
#     while True:
#         agent = random.choice(agents)
#         r = requests.get(link, headers={'User-agent': agent})
#         if r.status_code == 200:
#             break
#     soup = BeautifulSoup(r.text, 'html.parser')
#     for news in soup.select('h3[class=b] > a[href]'):
#         all_list.append(news['href'].encode("utf-8").decode()[2:])
#
# all_dict = [{'link': link} for link in all_list]
#
# with open('dirilis1.json', 'w') as fp:
#     json.dump(all_dict, fp)

with open('dirilis1.json', 'r') as fp:
    links = json.load(fp)

with open('dirilis2.json', 'w') as fp:
    fp.write('[\n' + ',\n'.join(json.dumps(i) for i in links) + '\n]')

