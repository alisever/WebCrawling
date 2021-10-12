import json
import pandas as pd

# df = pd.read_json('../old_files/Milliyet/milliyet9.json')
#
# df.to_excel('milliyet.xlsx', index=False)

with open('haberturk1.json') as fp:
    all_links = json.load(fp)

links = []
for item in all_links:
    link = item['link']
    if '.jpg' in link:
        continue
    if '.png' in link:
        continue
    if 'https://im.haberturk.com/' in link:
        continue
    if 'https://www.haberturk.com/' not in link:
        continue
    if 'https://www.haberturk.com/secim/secim2019/' in link:
        continue
    if 'https://www.haberturk.com/secim/secim2015/' in link:
        continue
    if 'https://www.haberturk.com/secim/secimAday2015/' in link:
        continue
    links.append({'link': link})

with open('haberturk_links.json', 'w') as fp:
    json.dump(links, fp)
