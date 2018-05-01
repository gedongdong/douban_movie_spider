# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 13:48
# @Contact : gedongdonghappy@gmail.com

import pymysql.cursors
from scrapy.utils.project import get_project_settings


class Db:
    connection = None

    def __init__(self):
        settings = get_project_settings()  # 获取settings配置，设置需要的信息
        self.connection = pymysql.connect(host=settings['MYSQL_HOST'],
                                          user=settings['MYSQL_USER'],
                                          password=settings['MYSQL_PASSWD'],
                                          db=settings['MYSQL_DBNAME'],
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def movie_insert(self, item):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `movie` (`douban_id`, `title`, `rate`, `cover`, `summary`) " \
                      "VALUES (%s, %s, %s, %s, %s)"
                params = (item['douban_id'], item['title'], item['rate'], item['cover'], item['summary'])
                cursor.execute(sql, params)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()

        finally:
            self.connection.close()

    def movie_update(self, item):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "UPDATE `movie` SET `summary`=%s WHERE `douban_id`=%s"
                params = (item['summary'], item['douban_id'])
                cursor.execute(sql, params)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()

        finally:
            self.connection.close()

    def comment_insert(self, item):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `movie_comments` (`douban_id`, `nickname`, `score`, `comment_time`, `content`)" \
                      " VALUES (%s, %s, %s, %s, %s)"
                params = (item['douban_id'], item['nickname'], item['score'], item['comment_time'], item['content'])
                cursor.execute(sql, params)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        finally:
            self.connection.close()
