# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    douban_id = scrapy.Field()
    rate = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
    summary = scrapy.Field()
    table_name = scrapy.Field()


class CommentItem(scrapy.Item):
    douban_id = scrapy.Field()
    nickname = scrapy.Field()
    score = scrapy.Field()
    comment_time = scrapy.Field()
    content = scrapy.Field()
    table_name = scrapy.Field()
