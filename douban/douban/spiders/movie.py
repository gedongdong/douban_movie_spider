# -*- coding: utf-8 -*-
import re

import requests
import scrapy
from bs4 import BeautifulSoup
from flask import json
from scrapy import Request
from douban.items import DoubanItem
from douban.items import CommentItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/']
    start_url = 'https://movie.douban.com/j/search_subjects?' \
                'type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}'
    summary_url = 'https://movie.douban.com/subject/{}/'
    page_start = 0
    comment_url = 'https://movie.douban.com/subject/{}/comments?' \
                  'start=20&limit=0&sort=new_score&status=P&percent_type='
    meta = {'dont_redirect': True, 'handle_httpstatus_list': [302], 'proxy': ''}
    cookies = {'dbcl2': '\"161732184:GuXvE+uB0g4\"'}

    def start_requests(self):
        yield Request(self.start_url.format(self.page_start), callback=self.parse, meta=self.meta, cookies=self.cookies)

    def parse(self, response):
        # 遇到302，使用代理重新请求
        if response.status == 302:
            self._get_proxy()
            yield Request(response.url, callback=self.parse, meta=self.meta, dont_filter=True, cookies=self.cookies)
        else:
            self.page_start += 20
            movie_json = json.loads(response.text)
            if movie_json['subjects']:
                for result in movie_json['subjects']:
                    item = DoubanItem()
                    item['douban_id'] = result.get('id')
                    item['rate'] = result.get('rate')
                    item['title'] = result.get('title')
                    item['cover'] = result.get('cover')
                    item['summary'] = False
                    item['table_name'] = 'movie'
                    # for field in item.fields:
                    #     if field in result.keys():
                    #         item[field] = result.get(field)

                    # 保存电影基本信息
                    yield item
                    # 保存电影摘要信息
                    yield Request(self.summary_url.format(result.get('id')),
                                  callback=self.parse_summary, meta=self.meta, cookies=self.cookies)
                    # 保存电影评论信息
                    yield Request(self.comment_url.format(result.get('id')),
                                  callback=self.parse_comment, meta=self.meta, cookies=self.cookies)
                yield Request(self.start_url.format(self.page_start), callback=self.parse,
                              meta=self.meta, cookies=self.cookies)

    def parse_summary(self, response):
        if response.status == 302:
            self._get_proxy()
            yield Request(response.url, callback=self.parse_summary,
                          meta=self.meta, dont_filter=True, cookies=self.cookies)
        else:
            result = re.findall('subject/(\d+)/', response.url)
            douban_id = result[0] if result[0] else 0

            if douban_id:
                item = DoubanItem()
                soup = BeautifulSoup(response.text, 'lxml')
                item['table_name'] = 'movie'
                item['douban_id'] = douban_id
                item['summary'] = soup.select('.related-info .indent span')[0].get_text().strip()
                yield item

    def parse_comment(self, response):
        if response.status == 302:
            self._get_proxy()
            yield Request(response.url, callback=self.parse_comment,
                          meta=self.meta, dont_filter=True, cookies=self.cookies)
        else:
            result = re.findall('subject/(\d+)/comments', response.url)
            douban_id = result[0] if result[0] else 0

            soup = BeautifulSoup(response.text, 'lxml')
            comments = soup.select('.comment-item')
            for comment in comments:
                comment_item = CommentItem()
                comment_item['nickname'] = comment.select('h3 .comment-info a')[0].get_text()
                comment_item['comment_time'] = comment.select('h3 .comment-info .comment-time')[0].attrs['title']
                try:
                    score_info = comment.select('h3 .comment-info .rating')[0].attrs['class']
                    score = score_info[0][-2:-1]
                except Exception:
                    score = 0
                comment_item['score'] = score
                comment_item['content'] = comment.select('p')[0].get_text().strip()
                comment_item['douban_id'] = douban_id
                comment_item['table_name'] = 'movie_comment'
                yield comment_item

            next_page = soup.select('#paginator .next')[0].attrs['href']
            if next_page:
                url = 'https://movie.douban.com/subject/{}/comments' + next_page
                yield Request(url.format(douban_id), callback=self.parse_comment,
                              meta=self.meta, dont_filter=True, cookies=self.cookies)

    def _get_proxy(self):
        proxy_pool_url = 'http://localhost:5555/random'
        try:
            response = requests.get(proxy_pool_url)
            if response.status_code == 200:
                self.meta['proxy'] = 'http://' + response.text
        except ConnectionError:
            return None
