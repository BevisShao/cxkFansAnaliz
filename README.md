# cxkFansAnaliz
a scrapy project which used to crawl cxk fans list through customed few middlewares including SpiderMiddleware and DownloadMiddleware.

## 简述
鉴于前端时间蔡徐坤刷榜引起的微博热点和微博文章的转发、评论数量造假事件，于是我突然萌生了一个利用数据揭示真相的想法。万里长征第一步，先要有抓取分析必备数据的能力。
之所以搭建scrapy项目，是考虑到后期需要的数据比较多，方便拓展分布式爬虫。

### Middleware
```python
# 'cxkFansAnaliz.middlewares.WeiboCookiesMiddleWare': 543
从cookies池获取有效cookies，给所有的Request对象赋值，实现免登录获取数据。

# 'cxkFansAnaliz.middlewares.CxkfansanalizDownloaderMiddleware': 542,
利用正则表达式处理微博的FM.view()问题，获取有效数据后，从新打包给Response对象，return出去。

# 'cxkFansAnaliz.middlewares.PhantomjsMiddleware': 542,
对接selenium自动登陆，利用browser对象的page_source属性重新赋值给Response，避免大量的处理页面问题，减少内存消耗；
同时，Phantomjs自带cookies和proxy属性，不用额外再写另两个中间件，减少维护成本；
```

### CxkfansanalizPipeline
```python
对接MongoDB，实现文档的批量插入；编写js脚本，实现数据库去重功能；
```

### meta:{'item':item}
```python
实现爬取多级页面的功能
```
