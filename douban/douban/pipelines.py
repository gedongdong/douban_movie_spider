# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from db.db import Db


class DoubanPipeline(object):

    def process_item(self, item, spider):
        db = Db()
        if item['table_name'] == 'movie':
            if item['summary']:
                db.movie_update(item)
            else:
                db.movie_insert(item)
        else:
            db.comment_insert(item)
        return item
