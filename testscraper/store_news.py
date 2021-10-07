import json
import pandas as pd

all_dicts = []
with open('milliyet_json_data.txt') as f:
    lines = f.readlines()
    for line in lines:
        line_dict = json.load(line)
        all_dicts.append(line_dict)

with open('milliyet.json', 'w') as f:
    json.dump(all_dicts, f)

# df = pd.read_json('yeni_akit1.json')
#
# df.to_excel('yeni_akit.xlsx', index=False)
