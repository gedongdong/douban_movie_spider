# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 13:48
# @Contact : gedongdonghappy@gmail.com

import pymysql.cursors


# def singleton(cls, *args, **kw):
#     instances = {}
#
#     def _singleton():
#         if cls not in instances:
#             instances[cls] = cls(*args, **kw)
#         return instances[cls]
#
#     return _singleton
#
#
# @singleton
class Db:
    connection = None

    def __init__(self):
        self.connection = pymysql.connect(host='127.0.0.1',
                                          user='root',
                                          password='root',
                                          db='movie',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def select_movie(self):
        try:
            sql = "SELECT `id`,`douban_id` FROM `movie` WHERE `id` > 230"
            cursor = self.connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception:
            self.connection.close()

    def select_comment(self, douban_id):
        try:
            sql = "SELECT `content` FROM `movie_comments` WHERE `douban_id`=%s"
            cursor = self.connection.cursor()
            cursor.execute(sql, (douban_id,))
            return cursor.fetchall()
        except Exception:
            self.connection.close()

    def movie_insert(self, item):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `movie` (`douban_id`, `title`, `rate`, `cover`) VALUES (%s, %s, %s, %s)"
                params = (item['douban_id'], item['title'], item['rate'], item['cover'])
                cursor.execute(sql, params)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()

            # with self.connection.cursor() as cursor:
            #     # Read a single record
            #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            #     cursor.execute(sql, ('webmaster@python.org',))
            #     result = cursor.fetchone()
            #     print(result)
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

            # with self.connection.cursor() as cursor:
            #     # Read a single record
            #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            #     cursor.execute(sql, ('webmaster@python.org',))
            #     result = cursor.fetchone()
            #     print(result)
        finally:
            self.connection.close()

