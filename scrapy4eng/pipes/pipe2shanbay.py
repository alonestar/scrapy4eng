# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import enchant
from scrapy4eng.data.words_sqlite_model import WordsSqliteModel
from scrapy4eng.data.dict_eng import DictEng
reload(sys)

class AlsScrapyShanbayPipeline(object):
    __dbModel = None
    __enchantObj = enchant.Dict("en_US")
    __dictEngObj = DictEng()

    def open_spider(self, spider):
        self.__dbModel = WordsSqliteModel()

    def process_item(self, item, spider):
        if spider.name == 'apache':
            for wordsline in item['body'].split("\n"):
                for words in wordsline.split(" "):
                    self.__checkAndAddWords(words)
        return item



    def __checkAndAddWords(self, newWords):
        newWords = newWords.lower()
        if newWords and self.__enchantObj.check(newWords) and self.__dictEngObj.isEnglishWord(newWords):
            self.__dbModel.replace_words(newWords)
            return True
        else:
            return False
