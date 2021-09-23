from json import load
import requests


with open('yenisafakhaberleri.json') as json_file:
    news_pages = load(json_file)
# TODO add these to a json and overwrite the old one
for index, item in enumerate(news_pages):
    if index < 5000:
        continue
    if index % 100 == 0:
        print(index)
    url = 'https://www.yenisafak.com/' + item['link']
    response = requests.get(url)
    if response.status_code == 200:
        pass
    else:
        url = 'https://www.yenisafak.com/gundem/' + item['link']
        response = requests.get(url)
        if response.status_code == 200:
            pass
        else:
            print("Could not find url for", item['link'])
