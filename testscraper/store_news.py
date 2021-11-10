import json
import pandas as pd

# months = ['',
#     'Ocak',
#     '\u015eubat',
#     'Mart',
#     'Nisan',
#     'May\u0131s',
#     'Haziran',
#     'Temmuz',
#     'A\u011fustos',
#     'Eyl\u00fcl',
#     'Ekim',
#     'Kas\u0131m',
#     'Aral\u0131k'
# ]
#
# dates = ['23 Eyl\u00fcl 2016 Cuma, 10:50', '08 Eyl\u00fcl 2021 \u00c7ar\u015famba']
#
#
# def date_cleaner(date):
#     if date[2] == '.':
#         return date.partition(' ')[0]
#     else:
#         start = ' '.join(date.split(' ')[:3])
#         split = start.split(' ')
#         converted = f'{split[0]}.{"0" * (2 - len(str(months.index(split[1]))))}{months.index(split[1])}.{split[2]}'
#         return converted
#
df = pd.read_json('tbmm2.json')

df.to_excel('tbmm2.xlsx', index=False)
