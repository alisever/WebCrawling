import pandas as pd

df = pd.read_json('old_files/Posta/posta_3.json')

# df = df[df['Detay'] == '']
# print(df.shape)
# print(df['Url'].iloc[1])

# df.to_excel('posta.xlsx', index=False)

# row = 3500
#
# print(df.iloc[row]['Url'])
# print(df.iloc[row]['Detay'])
