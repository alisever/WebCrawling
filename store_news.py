import pandas as pd

df = pd.read_json('./testscraper/ortadoguhaberleri.json')

df.replace('iremnur', 'İrem Nur Kaya', inplace=True)

df['Tarih'] = df['Tarih'].apply(lambda x: x[:-6])

# df.to_excel('ortadoguhaberleri.xlsx', index=False)
