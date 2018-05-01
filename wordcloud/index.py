# - * - coding: utf - 8 -*-
"""
create wordcloud with chinese
=======================

Wordcloud is a very good tools, but if you want to create
Chinese wordcloud only wordcloud is not enough. The file
shows how to use wordcloud with Chinese. First, you need a
Chinese word segmentation library jieba, jieba is now the
most elegant the most popular Chinese word segmentation tool in python.
You can use 'PIP install jieba'. To install it. As you can see,
at the same time using wordcloud with jieba very convenient
"""
from os import path
from random import choice

from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib
import jieba

import db


class WordCloudImg:
    douban_id = ''
    text = ''
    stopwords_path = ''
    font_path = ''
    back_coloring = ''
    d = ''

    def __init__(self, douban_id, text):
        self.text = text
        self.douban_id = douban_id
        self.d = path.dirname(__file__)
        self.stopwords_path = self.d + 'wc_cn/stopwords_cn_en.txt'
        # Chinese fonts must be set
        self.font_path = self.d + 'fonts/SourceHanSerif/SourceHanSerifK-Light.otf'

        img_num = str(choice(range(1, 11)))
        self.back_coloring = imread(path.join(self.d, self.d + 'wc_cn/' + img_num + '.jpg'))

        # Setting up parallel processes :4 ,but unable to run on Windows
        jieba.enable_parallel(4)
        matplotlib.use('TkAgg')

        # Read the whole text.
        # self.text = open(path.join(self.d, self.d + 'wc_cn/CalltoArms.txt')).read()
        self.word_cloud_img()

    def jieba_processing_txt(self):
        userdict_list = ['小戏骨']
        for word in userdict_list:
            jieba.add_word(word)
        mywordlist = []
        seg_list = jieba.cut(self.text, cut_all=False)
        liststr = "/ ".join(seg_list)

        with open(self.stopwords_path, encoding='utf-8') as f_stop:
            f_stop_text = f_stop.read()
            f_stop_seg_list = f_stop_text.split('\n')

        for myword in liststr.split('/'):
            if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
                mywordlist.append(myword)
        return ' '.join(mywordlist)

    def word_cloud_img(self):
        wc = WordCloud(font_path=self.font_path, background_color="white", max_words=5000, mask=self.back_coloring,
                       max_font_size=40, random_state=52, width=1000, height=860, margin=1, )

        wc.generate(self.jieba_processing_txt())

        # create coloring from image
        image_colors_by_img = ImageColorGenerator(self.back_coloring)
        wc.recolor(color_func=image_colors_by_img)
        wc.to_file(path.join(self.d, 'comment_img/' + str(self.douban_id) + '.png'))


db = db.Db()
movie = db.select_movie()
i = 0
for douban_id in movie:
    print(str(douban_id['id'])+': '+str(douban_id['douban_id'])+'running...')
    content = db.select_comment(douban_id=douban_id['douban_id'])
    text = [t['content'] for t in content]
    text = '。'.join(text)
    WordCloudImg(douban_id=douban_id['douban_id'], text=text)
    print(str(douban_id['douban_id'])+'succ')
    i += 1
print('total:' + str(i))
