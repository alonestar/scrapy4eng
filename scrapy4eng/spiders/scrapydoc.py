# -*- coding: utf-8 -*-
import scrapy
import time
import re
import urlparse

from bs4 import BeautifulSoup
from scrapy4eng.items.scrapydoc import ScrapyDocItem

class ScrapydocSpider(scrapy.Spider):
    name = 'scrapydoc'
    allowed_domains = ['docs.scrapy.org']
    start_urls = ['https://docs.scrapy.org/en/latest']
    __reAllownUrl = re.compile(r'.*docs.scrapy.org.*')
    __scanUrl = start_urls;

    def parse(self, response):
        self.__log('parse|' + response.url)
        soup = BeautifulSoup(response.body, "lxml")

        item = ScrapyDocItem()
        item['url'] = response.url
        item['title'] = soup.title.get_text()
        item['body'] = soup.find(attrs={"itemprop": "articleBody"}).get_text(' ', strip=True)
        yield item

        for a in soup.find(class_='wy-menu').find_all("a"):
            urlTmp = urlparse.urljoin(response.url, a.attrs['href'].strip())

            yield scrapy.http.Request(urlTmp)
            # if self.__checkAppendUrl(urlTmp):
            #     yield scrapy.http.Request(urlTmp)
            #     pass

    def __log(self, logStr):
        logPre = "[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "] "
        print logPre + str(logStr) + '|';

    def __checkAppendUrl(self, urlStr):
        urlStr = urlStr.strip('/')
        if urlStr in self.__scanUrl:
            # self.__log('[exist]'+urlStr)
            return False;

        if self.__reAllownUrl.match(urlStr):
            self.__scanUrl.append(urlStr)
            # self.start_urls.append(urlStr)
            return True;
        return False;
