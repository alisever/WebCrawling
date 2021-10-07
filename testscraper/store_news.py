import json
import pandas as pd

all_dicts = []
with open('milliyet_json_data.txt', encoding="utf8") as f:
    lines = f.readlines()
    for line in lines:
        line_dict = json.loads(line)
        all_dicts.append(line_dict)

with open('milliyet.json', 'w') as f:
    json.dump(all_dicts, f, indent=4)

# df = pd.read_json('yeni_akit1.json')
#
# df.to_excel('yeni_akit.xlsx', index=False)
