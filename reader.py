#! /usr/bin/python
# -*- coding:utf-8 -*-
import json
from header import *
import pymongo
from datetime import *
import time
from pymongo import MongoClient

class Reader():
    def __init__(self, uri):
        self._db_name = "NES"
        self._news_collection_name = "news"
        self._event_collection_name = "event"
        self.client = MongoClient(uri)
        self.db = self.client[self._db_name]

    def parse_uri(self, host, username, pswd):
        uri = "mongodb://" + username + ":" + pswd + "@" + host + "?authSource=source"
        return uri

    def time2time_stamp(self, t):
        timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        timeStamp = float(time.mktime(timeArray))
        return timeStamp

    def time_stamp2time(self, t):
        return str(datetime.fromtimestamp(t))

    def remove_mongoDB(self):
        pass

    def insert_mongoDB(self, news):
        pass

    def query_mongoDB_by_time(self, start_time, end_time):
        pass

    def query_mongoDB_by_item(self, item):
        pass

    def read_txt(self, filename):
        with open(filename, "r") as f:
            return json.loads(f.read())

class NewsReader(Reader):
    def __init__(self, uri):
        Reader.__init__(self, uri=uri)
        self.init_mongoDB()

    def init_mongoDB(self):
        """
        初始化mongoDB, 包含client, db, collection
        :param uri: 輸入mongoDB的uri位址
        :return: none
        """
        self.news_collection = self.db[self._news_collection_name]
        print self.db
        print self.news_collection

    def remove_mongoDB(self):
        self.news_collection.remove()

    def test(self):
        result = self.news_collection.find()
        for i in result:
            print i

    def insert_mongoDB(self, news):
        result = self.news_collection.insert(news)
        return result

    def query_mongoDB_by_time(self, start_time, end_time):
        """
        尋找mongoDB news collection中符合時間段內的新聞
        :param start_time: 開始時間 (上次查詢後最後時間)
        :param end_time: 結束時間 (time.time() 現在運行時間)
        :return: result: 查詢結果
        """
        result = self.news_collection.find({"crawlTime": {"$gt": start_time, "$lt": end_time}})
        # for i in result:
        #     print i
        return result

    def query_mongoDB_by_item(self, item):
        """
        根據提供的item尋找mongoDB news collection中符合的新聞
        :param item: 查詢的item條件, dict
        :return: result: 查詢結果
        """
        result = self.news_collection.find(item)
        # for i in result:
        #     print i
        return result

class EventReader(Reader):
    def __init__(self, uri):
        Reader.__init__(self, uri=uri)
        self.init_mongoDB()
        self.day_diff = 86400
        self.window = 7

    def init_mongoDB(self):
        """
        初始化mongoDB, 包含client, db, collection
        :param uri: 輸入mongoDB的uri位址
        :return: none
        """
        self.event_collection = self.db[self._event_collection_name]
        print self.db
        print self.event_collection

    def remove_mongoDB(self):
        self.event_collection.remove()

    def test(self):
        result = self.event_collection.find()
        for i in result:
            print i

    def insert_mongoDB(self, news):
        result = self.event_collection.insert(news)
        return result

    def create_event_id(self, current_time):
        """

        :param current_time: 2016-06-20 17:00:00
        :return: eid: 20170620170000
        """
        eid = current_time.replace('-', '')
        eid = eid.replace(':', '')
        eid = eid.replace(' ', '')
        return eid

    def query_recent_events(self, current_time):
        last_time = int(Reader.time2time_stamp(self, current_time) - self.day_diff * self.window)
        last_time = Reader.time_stamp2time(self, last_time)
        return self.query_mongoDB_by_time(start_time=last_time, end_time=current_time)

    def query_mongoDB_by_time(self, start_time, end_time):
        """
        尋找mongoDB event collection中符合時間段內的新聞
        :param start_time: 開始時間 (上次查詢後最後時間)
        :param end_time: 結束時間 (time.time() 現在運行時間)
        :return: result: 查詢結果
        """
        result = self.event_collection.find({"updated": {"$gt": start_time, "$lt": end_time}})
        # for i in result:
        #     print i
        return result

    def query_mongoDB_by_item(self, item):
        """
        根據提供的item尋找mongoDB news collection中符合的新聞
        :param item: 查詢的item條件, dict
        :return: result: 查詢結果
        """
        result = self.event_collection.find(item)
        # for i in result:
        #     print i
        return result

if __name__ == "__main__":
    # news_reader = NewsReader(uri='localhost')
    # news_list = news_reader.query_mongoDB_by_time(start_time="2016-11-20 16:00:00", end_time="2016-11-20 18:00:00")
    event_reader = EventReader(uri='localhost')
    event_reader.query_recent_events(current_time="2016-11-20 16:00:00")