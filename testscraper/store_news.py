import json
import pandas as pd

df = pd.read_json('../old_files/Milliyet/milliyet9.json')

df.to_excel('milliyet.xlsx', index=False)
