# -*- coding: utf-8 -*-
import scrapy
import time
import re
import urlparse
import urllib2

from bs4 import BeautifulSoup
from scrapy4eng.items.article import ArticleItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['http://www.cnblogs.com/']
    __reAllownUrl = [
        # re.compile(r'.*www.cnblogs.com.*'),
        re.compile(r'.*www.cnblogs.com/\#.*'),
        re.compile(r'.*www.cnblogs.com/.*/\#.*'),
        re.compile(r'.*www.cnblogs.com/.*/category/.*\.html'),
        re.compile(r'.*www.cnblogs.com/.*/p/'),
        re.compile(r'.*www.cnblogs.com/cate/.*/'),
        re.compile(r'.*www.cnblogs.com/.*/$'),
        re.compile(r'.*www.cnblogs.com/.*/tag/.*/'),
    ]
    __reArticlePage = re.compile('http://www.cnblogs.com/.*/p/')
    __reFindAuthorId = re.compile('.*www.cnblogs.com/([^/]*)/.*')
    __reFindPageId = re.compile('.*postid=([0-9]*)')
    __reFindTime = re.compile('(.*) by.*')
    __scanUrl = start_urls;

    __scanNum = 0;
    __scanAllNum = 0;
    __scanMaxNum = 100000;
    __scanErrorNum = 0;

    def parse(self, response):
        self.__scanAllNum += 1;
        # self.__log('parse|' + str(self.__scanNum) + '/' + str(self.__scanAllNum) + '|' + response.url)
        soup = BeautifulSoup(response.body, "lxml")

        if self.__isArticlePage(response.url):
            self.__scanNum += 1;
            if self.__scanNum % 10 == 0 :
                self.__log('articlePage|' + str(self.__scanNum) + '/' + str(self.__scanErrorNum) + '/' + str(self.__scanAllNum) + '|' + response.url)

            item = ArticleItem()
            item['channel'] = self.name
            item['url'] = response.url
            item['title'] = soup.title.get_text()
            item['aid'] = 0
            item['view_count'] = 0
            item['author'] = ''
            item['body'] = item['title']
            item['post_time'] = '1970-01-01 08:00:00'

            try:
                nofollowA = soup.select("div.postDesc > a[rel='nofollow']")
                if len(nofollowA):
                    pageId = self.__reFindPageId.findall(nofollowA[0].attrs['href'])[0]
                elif soup.find(id='post-date'):
                    nofollowA = soup.find(id='post-date').parent.select("a[rel='nofollow']")
                    pageId = self.__reFindPageId.findall(nofollowA[0].attrs['href'])[0]
                else:
                    nofollowA = soup.select("div#post_detail > div > small > a[rel='nofollow']")
                    pageId = self.__reFindPageId.findall(nofollowA[0].attrs['href'])[0]
                response4ViewCount = urllib2.urlopen('http://www.cnblogs.com/mvc/blog/ViewCountCommentCout.aspx?postId='+pageId)
                item['aid'] = pageId
                item['view_count'] = response4ViewCount.read()
                item['result'] = 200
            except:
                self.__scanErrorNum += 1;
                item['result'] = 501

            try:
                if soup.find('a', class_='headermaintitle'):
                    item['author'] = soup.find('a', class_='headermaintitle').get_text(' ', strip=True)
                else:
                    item['author'] = self.__reFindAuthorId.findall(response.url)[0]
            except:
                self.__scanErrorNum += 1;
                item['result'] = 502

            try:
                item['body'] = soup.find('a', id="cb_post_title_url").get_text(' ', strip=True)
            except:
                self.__scanErrorNum += 1;
                item['result'] = 503

            try:
                if soup.find(id='post-date'):
                    for string in soup.find(id='post-date').stripped_strings:
                        item['post_time'] = string
                        break;
                else:
                    timeStr = soup.select("div#post_detail > div > small")[0].get_text(' ', strip=True)
                    item['post_time'] = self.__reFindTime.findall(timeStr)[0]
            except:
                self.__scanErrorNum += 1;
                item['result'] = 504

            if item['result'] != 200:
                print item
            yield item

        for a in soup.body.find_all("a"):
            if a.attrs.has_key('href') and self.__checkAllowUrl(a.attrs['href'].strip()) and self.__scanNum <= self.__scanMaxNum:
                urlTmp = urlparse.urljoin(response.url, a.attrs['href'].strip())
                yield scrapy.http.Request(urlTmp)

    def __log(self, logStr):
        logPre = "[" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "] "
        print logPre + str(logStr) + '|';

    def __checkAllowUrl(self, urlStr):
        # urlStr = urlStr.strip('/')
        _rtnBool = False;

        for reCompile in self.__reAllownUrl:
            if reCompile.match(urlStr):
                _rtnBool = True;
                break;
        if _rtnBool == False and re.compile(r'.*www.cnblogs.com.*').match(urlStr):
            if re.compile(r'.*[(archive)|(rss)].*').match(urlStr):
                pass
            else:
                self.__log('reFail|'+urlStr)
                print urlStr;
        return _rtnBool;
        # if self.__reAllownUrl.match(urlStr):
        #     return True;
        # else:
        #     return False;

    def __isArticlePage(self, urlStr):
        if self.__reArticlePage.match(urlStr):
            return True
        else:
            return False
