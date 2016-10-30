import datetime
from tinydb import TinyDB, where, Query
import json

class Database():
    def __init__(self, db_path):
        self.db = TinyDB(db_path)

    def add_deal(self, deal):
        deal['date'] = str(datetime.datetime.utcnow())
        print(deal['date'])
        self.db.insert(deal)

    def match_old_deal(self, url, title, firstpostdate):
        deal = Query()
        result = self.db.search(deal.url == url)
        if not result:
            result = self.db.search((deal.title == title) & (deal.firstpostdate == firstpostdate))
            if not result:
                return False
        return True
