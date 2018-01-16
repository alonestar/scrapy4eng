# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
import sys
import time
import os
reload(sys)
sys.setdefaultencoding( "utf-8" )

class AlsScrapyTxtPipeline(object):
    __base = os.path.abspath('.') + '/data/txt'
    __base = os.path.dirname(__file__) + '/../data/txt/'

    def open_spider(self, spider):
        timeStr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.file = open(self.__base+'/'+spider.name+'_'+timeStr+'.log', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        _writeStr = ''
        if spider.name == 'apache':
            _writeStr = str(item['url']) + ' | ' + str(item['title']) + "\n" + str(item['body']) + "\n"
        else:
            pass

        if _writeStr:
            self.file.write(_writeStr);
        return item
