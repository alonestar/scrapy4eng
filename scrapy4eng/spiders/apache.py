# -*- coding: utf-8 -*-
import scrapy
import time
import re
import urlparse

from bs4 import BeautifulSoup
from scrapy4eng.items.article import ArticleItem

class ApacheSpider(scrapy.Spider):
    name = 'apache'
    allowed_domains = ['www.apache.com', 'blogs.apache.org']
    start_urls = ['http://www.apache.com', 'http://blogs.apache.org']
    __scanNum = 1
    __maxScanNum = 10000

    def parse(self, response):
        self.__log("[parse] %d|%d|%s" % (self.__maxScanNum, self.__scanNum, response.url))
        soup = BeautifulSoup(response.body, "lxml")

        item = ArticleItem()
        item['url'] = response.url
        item['title'] = soup.title.get_text()
        if soup.article:
            item['body'] = soup.article.get_text(' ', strip=True)
        else:
            item['body'] = soup.body.get_text(' ', strip=True)
        yield item

        for a in soup.find_all('a'):
            if 'href' in a.attrs:
                urlTmp = urlparse.urljoin(response.url, a.attrs['href'].strip())
                if self.__scanNum <= self.__maxScanNum:
                    yield scrapy.http.Request(urlTmp)
                    self.__scanNum += 1

    def __log(self, logStr):
        logPre = "[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "] "
        print logPre + str(logStr) + '|';

