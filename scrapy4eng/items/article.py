# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    channel = scrapy.Field()
    aid = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    post_time = scrapy.Field()
    view_count = scrapy.Field()
    result = scrapy.Field()
    pass
