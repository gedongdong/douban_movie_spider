# douban_movie_spider 豆瓣电影抓取和WordCloud生成

## 运行步骤

### 1. 首先进入ProxyPool，根据ReadMe文件运行代理（需要安装Redis服务）

### 2. 进入douban，修改settings.py中mysql配置信息，然后执行scrapy crawl movie，开始数据抓取（movie.py中的cookies需要自行登录豆瓣获取到cookie即可）

### 3. 数据抓取完毕后，进入wordcloud，运行python index.py，开始生成云词图

## 表结构

movie表：
```
CREATE TABLE `movie` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `douban_id` int(10) unsigned NOT NULL DEFAULT '0',
  `title` varchar(50) CHARACTER SET utf8mb4 NOT NULL DEFAULT '' COMMENT '标题',
  `rate` float NOT NULL DEFAULT '0' COMMENT '评分',
  `cover` varchar(200) CHARACTER SET utf8mb4 NOT NULL DEFAULT '' COMMENT '封面图',
  `summary` text COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT '摘要',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=327 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
```

movie_comments表：
```
CREATE TABLE `movie_comments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `douban_id` int(10) unsigned NOT NULL DEFAULT '0',
  `nickname` varchar(50) CHARACTER SET utf8mb4 NOT NULL DEFAULT '' COMMENT '用户名',
  `score` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '评分',
  `comment_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '评论日期',
  `content` text CHARACTER SET utf8mb4 NOT NULL COMMENT '评论内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=145765 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
```
