# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AllUrlsPipeline:
    def __init__(self):
        self.con = sqlite3.connect('sozcu.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS urls (
        url TEXT PRIMARY KEY,
        keyword INTEGER  
        )""")

    def process_item(self, item, spider):
        self.cur.execute("""INSERT OR IGNORE INTO urls VALUES (?,?)""",
                         (item['url'], item['keyword']))
        self.con.commit()
        return item
