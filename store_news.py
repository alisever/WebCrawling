import pandas as pd
import json
df = pd.read_json('./testscraper/yenisafak_4.json')

df = df[df['Detay'] != '']

print(df.shape)
print(len(df['Url'].unique()))

df.to_excel('yenisafak.xlsx', index=False)
