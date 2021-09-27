import pandas as pd
import json
df = pd.read_json('./testscraper/posta_2.json')

df = df[df['Detay'] == '']
print(df.shape)
print(df['Url'].iloc[1])

# df.to_excel('posta.xlsx', index=False)
