from json import load, dump
import requests

with open('yenisafak_missing.json') as json_file:
    # news_pages = json_file.read()
    news_pages = load(json_file)

with open('yenisafak_missing_clean.json', 'w') as json_file:
    # json_file.write(news_pages)
    dump(news_pages, json_file, indent=4)
exit()
# with open('old_files/yenisafakhaberleri.json') as json_file:
#     news_pages = load(json_file)
#
# with open('old_files/yenisafak_cleaned.csv', 'r') as file:
#     fixed = file.read()
#
# cleaned_pages = []
#
# for index, item in enumerate(news_pages):
#     if index % 100 == 0:
#         print(index)
#     url = 'https://www.yenisafak.com/' + item['link']
#     if url in fixed:
#         cleaned_pages.append({'link': url, 'type': item['type']})
#         continue
#     try:
#         response = requests.get(url)
#     except requests.exceptions.TooManyRedirects:
#         pass
#     else:
#         if response.status_code == 200:
#             cleaned_pages.append({'link': url, 'type': item['type']})
#             continue
#     url = 'https://www.yenisafak.com/gundem/' + item['link']
#     if url in fixed:
#         cleaned_pages.append({'link': url, 'type': item['type']})
#         continue
#     response = requests.get(url)
#     if response.status_code == 200:
#         cleaned_pages.append({'link': url, 'type': item['type']})
#     else:
#         print({'link': url, 'type': item['type']})
#
# cleaned_pages = [dict(t) for t in {tuple(d.items()) for d in cleaned_pages}]
#
# with open('old_files/yenisafak_cleaned.json', 'w') as json_file:
#     dump(cleaned_pages, json_file)
