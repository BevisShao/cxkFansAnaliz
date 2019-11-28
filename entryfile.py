# 添加本文件使IDE可以自动运行爬虫
from scrapy.cmdline import execute
# execute(['scrapy', 'crawl', 'quotes', '-o', 'quotes.json'])     # 此命令行的意义是：用scrapy提供的Feed Exports模块方便的存储到文件，如果是大型项目，需要使用Item Pileline来完成数据持久化。
execute(['scrapy', 'crawl', 'cxkFans'])


