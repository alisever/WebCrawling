import csv
import multiprocessing
from json import load, dumps
import requests
import codecs

with codecs.open('yenisafakhaberleri.json', encoding='utf-8') as json_file:
    news_pages = load(json_file)

with open('yenisafak_cleaned.csv', 'r') as file:
    # fixed = "".join(line for line in file if line.startswith('https'))
    fixed = file.read()

# with open('yenisafak_cleaned_1.csv', 'w') as fd:
#     fd.write(fixed)

# with open('yenisafak_cleaned.csv') as result:
#     uniqlines = set(result.readlines())
#     with open('yenisafak_cleaned_1.csv', 'w') as rmdup:
#         rmdup.writelines(set(uniqlines))


def write_file(new_data, filename='yenisafak_cleaned.txt'):
    with open(filename, 'a') as my_file:
        my_file.write('\n')
        my_file.write(new_data)


def cleaner(argument):
    index, item = argument
    if index % 100 == 0:
        print(index)
    if item['link'] in fixed:
        write_file(dumps(item))
        return None
    url = 'https://www.yenisafak.com/' + item['link']
    try:
        response = requests.get(url)
    except requests.exceptions.TooManyRedirects:
        pass
    else:
        if response.status_code == 200:
            write_file(dumps({'link': url, 'type': item['type']}))
            return None

    url = 'https://www.yenisafak.com/gundem/' + item['link']
    response = requests.get(url)
    if response.status_code == 200:
        write_file(dumps({'link': url, 'type': item['type']}))
    else:
        print({'link': url, 'type': item['type']})


if __name__ == '__main__':
    p = multiprocessing.Pool()
    p.map(cleaner, enumerate(news_pages))
