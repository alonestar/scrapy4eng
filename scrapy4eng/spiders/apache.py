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

    def parse(self, response):
        self.__log('parse|' + response.url)
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
                yield scrapy.http.Request(urlTmp)

    def __log(self, logStr):
        logPre = "[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "] "
        print logPre + str(logStr) + '|';

