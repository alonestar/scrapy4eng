# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import sys
import time
reload(sys)
from scrapy.exceptions import DropItem

class AlsScrapyMysqlPipeline(object):
    __batch = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    __insertNum = 0;

    def __init__(self):
        try:
            self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456789", port=3306, db="als_scrapy",  charset="utf8")
            self.cursor = self.db.cursor()
            print "Connect to db successfully!"

        except:
            print "Fail to connect to db!"

    def close_spider(self, spider):
        self.db.commit()
        self.db.close
        print("Done")

    def process_item(self, item, spider):
        if spider.name != 'cnblogs':
            return item

        if item['title']:
            param = (self.__batch, item['channel'], item['aid'], item['url'], item['author'], item['body'], item['post_time'], item['view_count'], item['result'])
            sql = "insert into article(batch, channel, aid, url, author, title, post_time, view_count, result) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql, param)
            self.__insertNum += 1;
            if self.__insertNum % 100 == 0:
                self.db.commit()

        else:
            raise DropItem(item)

        return item
