# -*- coding: utf-8 -*-

# Scrapy settings for cxkFansAnaliz project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'cxkFansAnaliz'

DOMAIN_HOST = 'https://weibo.com'

SPIDER_MODULES = ['cxkFansAnaliz.spiders']
NEWSPIDER_MODULE = 'cxkFansAnaliz.spiders'

# scrapy-redis
# 调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 调度队列
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.PriorityQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.FifoQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.LifoQueue"

# 持久化
# 默认是False，scrapy-redis会在爬取完成后清空队列和去重指纹集合。如果不想清空，设置为True。
# 强制中断爬虫运行不会自动清空。
# SCHEDULER_PERSIST = True

# 配置重爬
# 默认False。 如果配置了持久化或者强制中断爬虫，结合不被清空，那么重启后会接着上次爬取，
# 但是如果想重新爬取，就设置为True。
# SCHEDULER_FLUSH_ON_START = True



WEIBO_COOKIES_URL = 'http://localhost:5000/weibo/random'
# WEIBO_COOKIES_URL = 'cookiespool:5000/weibo/random'
REDIRECT_ENABLED = True
# COOKIES_DEBUG = True
SELENIUM_TIMEOUT = 10
service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']
# Redis数据库地址
# REDIS_HOST = '127.0.0.1'
REDIS_HOST = '192.168.0.112'
# Redis端口
REDIS_PORT = 6379
# Redis密码，如无填None
REDIS_PASSWORD = None
REDIS_KEY = 'cookies:weibo'

PHANTOMJS_HOST_DOCKER = 'phantomjs_cxk'

MONGO_URI = 'localhost'
MONGO_URI_DOCKER = 'mongodb'
MONGO_DATABASE = 'cxkFans'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cxkFansAnaliz (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'cxkFansAnaliz.middlewares.CxkfansanalizSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'cxkFansAnaliz.middlewares.WeiboCookiesMiddleWare': 543,
   'cxkFansAnaliz.middlewares.CxkfansanalizDownloaderMiddleware': 542,
   # 'cxkFansAnaliz.middlewares.PhantomjsMiddleware': 541,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'cxkFansAnaliz.pipelines.CxkfansanalizPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
