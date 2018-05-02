# douban_movie_spider 豆瓣电影抓取和WoldCloud生成

## 运行步骤

### 1. 首先进入ProxyPool，根据ReadMe文件运行代理（需要安装Redis服务）

### 2. 进入douban，修改settings.py中mysql配置信息，然后执行scrapy crawl movie，开始数据抓取（movie.py中的cookies需要自行登录豆瓣获取到cookie即可）

### 3. 数据抓取完毕后，进入wordcloud，运行python index.py，开始生成云词图
