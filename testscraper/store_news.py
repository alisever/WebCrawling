import json
import pandas as pd

# df = pd.read_json('../old_files/Milliyet/milliyet9.json')
#
# df.to_excel('milliyet.xlsx', index=False)
df = pd.read_csv('../sara_bareilles.csv')
print(df['name'])
df['name'].to_csv('../sara_songs.csv', index=False)
