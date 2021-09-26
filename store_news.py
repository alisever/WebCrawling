import pandas as pd
import json
df = pd.read_json('./testscraper/yenisafak_2.json')

df = df[df['Detay'] == '']['Url']
missing = list(df)
print(missing[0:10])

with open('testscraper/yenisafak_missing.json', 'w') as json_file:
    json.dump(missing, json_file)
# df.to_excel('ortadoguhaberleri.xlsx', index=False)
