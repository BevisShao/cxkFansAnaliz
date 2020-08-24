# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import logging
import re
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
import requests
from scrapy import signals
from scrapy.http import HtmlResponse
import redis
import random, os
from cxkFansAnaliz.settings import PHANTOMJS_HOST_DOCKER


class CxkfansanalizSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class PhantomjsMiddleware(object):
    host = os.environ.get('ISDOCKER')
    caps = DesiredCapabilities.PHANTOMJS
    caps["phantomjs.page.settings.userAgent"] = \
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'

    def __init__(self, timeout, REDIS_KEY, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD):
        # 设置浏览器请求头
        self.db_redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
        self.REDIS_KEY = REDIS_KEY
        self.logger = logging.getLogger('PhantomjsMiddleWare')
        self.timeout = timeout
        self.logger.info('host = {}'.format(self.host))
        if self.host:
            self.browser = webdriver.Remote(
                # command_executor='http://192.168.0.112:8910', desired_capabilities=caps)
                command_executor='http://{}:8911'.format(PHANTOMJS_HOST_DOCKER), desired_capabilities=self.caps)
            # command_executor='http://phantomjs:8910', desired_capabilities=caps)

        else:
            self.browser = webdriver.PhantomJS(desired_capabilities=self.caps)
        self.browser.maximize_window()
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # self.browser = webdriver.Chrome(executable_path=r'E:\InstallLocation\Chrome\_71_0_3578\chromedriver.exe', options=chrome_options)
        # self.browser = webdriver.Chrome(options=chrome_options)
        self.dict_cookies = self.get_random_cookies()
        self.wait = WebDriverWait(self.browser, self.timeout)

    def get_random_cookies(self):
        list_keys = self.db_redis.hkeys(self.REDIS_KEY)
        print(list_keys)
        assert list_keys, self.logger.warning('当前cookies池为空...')
        if list_keys:
            key_random = random.choice(list_keys)
            value_random = self.db_redis.hget(self.REDIS_KEY, key_random)
            print('当前获取的cookies：{}'.format(value_random))
            cookies = json.loads(value_random)
            return cookies
        else:
            self.logger.warning('获取cookies失败...')

    # def get_random_cookies(self):
    #     try:
    #         response = requests.get(self.cookies_pool_url)
    #     except Exception as e:
    #         self.logger.info('scarpy 获取随机cookies失败 {}'.format(e))
    #     else:
    #         cookies = json.loads(response.text)
    #         self.logger.info('scarpy 获取随机cookies成功:{}'.format(response.text))
    #         return cookies

    def __del__(self):
        if self.__dict__.get('browser'):
            self.browser.close()

    def process_request(self, request, spider):
        '''
        :param request: Request 对象
        :param spider: Spider 对象
        :return: HtmlResponse
        '''
        try:
            self.browser.get(request.url)
            for cookie_name, cookie_value in self.dict_cookies.items():
                try:
                    self.browser.add_cookie({
                        #         'version':0,
                        'domain': 'weibo.com',
                        #         'httpOnly': False,
                        'name': cookie_name,
                        'value': cookie_value,
                        # 'expiry': None,
                        'secure': True,
                        # 'path': '/'
                    })
                except exceptions.UnableToSetCookieException:
                    pass
                    # self.logger.warning('填充cookies的时候曾经出现格式错误(UnableToSetCookieException)...')
            print('PhantomjsMiddleware.process_request()..')
            # self.wait.until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, '.follow_inner .follow_list'))
            # )
            print('page_source:\n{}'.format(self.browser.page_source))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request,
                                encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):     # 一种依赖注入，从配置文件里读取参数
        # print(crawler.settings.get('SERVICE_ARGS'))
        return cls(
            timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
            # cookies_pool_url=crawler.settings['WEIBO_COOKIES_URL'],
            REDIS_KEY=crawler.settings['REDIS_KEY'],
            REDIS_HOST=crawler.settings['REDIS_HOST'],
            REDIS_PORT=crawler.settings['REDIS_PORT'],
            REDIS_PASSWORD=crawler.settings['REDIS_PASSWORD']
            # service_args=crawler.settings.get('SERVICE_ARGS')
        )


class WeiboCookiesMiddleWare(object):
    def __init__(self, cookies_pool_url):
        self.logging = logging.getLogger('WeiboMiddleWare')
        self.cookies_pool_url = cookies_pool_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_pool_url)
        except Exception as e:
            self.logging.info('scarpy 获取随机cookies失败 {}'.format(e))
        else:
            cookies = json.loads(response.text)
            self.logging.info('scarpy 获取随机cookies成功:{}'.format(response.text))
            return cookies

    @classmethod
    def from_settings(cls, settings):
        obj = cls(
            cookies_pool_url=settings['WEIBO_COOKIES_URL']
        )
        return obj

    def process_request(self, request, spider):
        request.cookies = self.get_random_cookies()
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

        return None

    def process_response(self, request, response, spider):
        """
        对此次请求的响应进行处理。
        :param request:
        :param response:
        :param spider:
        :return:
        """
        # 携带cookie进行页面请求时，可能会出现cookies失效的情况。访问失败会出现两种情况：1. 重定向302到登录页面；2. 也能会出现验证的情况；
        # 想拦截重定向请求，需要在settings中配置。
        print("当前响应码：{}".format(response.status))
        print('响应文本:{}'.format(response.body))
        with open('302.html', 'wb') as f:
            f.write(response.body)
        if response.status in [302, 301]:
            # 如果出现了重定向，获取重定向的地址
            redirect_url = response.headers['location']
            print("当前响应码：{}".format(response.status))
            # print('响应文本:{}'.format(response.body))
            if 'passport' in redirect_url:
                # 重定向到了登录页面，Cookie失效。
                self.logging.info('Cookies Invaild!')
                # TODO
                # 需要重新获得cookies
            elif '验证页面' in redirect_url:
                # Cookies还能继续使用，针对账号进行的反爬虫。
                self.logging.info('当前Cookie无法使用，需要认证。')
            elif redirect_url == 'https://weibo.com':
                return response
            # 如果出现重定向，说明此次请求失败，继续获取一个新的Cookie，重新对此次请求request进行访问。
            # request.cookies = self.get_random_cookies()
            # 返回值request: 停止后续的response中间件，而是将request重新放入调度器的队列中重新请求。
            else:
                return request
        elif response.status == 200:
            # redirect_url = response.headers[b'location']
            if 'passport' in response.url:
                return request
            else:
                return response
        elif response.status == 500:
            return request
        # #  ，直接将response向下传递后续的中间件。
        # return response


class CxkfansanalizDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        contents = response.text
        contents_re = re.search('欧盟隐私协议弹窗.*?>(.*?)</html>', contents, re.S)
        results = contents_re.group(1)
        print('downloadmiddleware里的response{}'.format(results))
        htmls = []
        patterns1 = re.compile('.*?<script>FM\.view\((.*?)\)</script>', re.S)
        patterns2 = re.compile('\t*\n*\r*', re.S)
        scripts = re.findall(patterns1, results)
        if scripts:
            print(scripts)
            for script in scripts:
                print('获得的scrpt:{}'.format(script))
                html = (json.loads(script)).get('html')
                if html:
                    html_re = re.sub(patterns2, '', html)
                    htmls.append(html_re)
                # htmls.append((json.loads(scripts.lstrip('<script>FM.view(').rstrip(')</script>')).get('html')).replace(r'\r', '').replace(r'\n', '').replace(r'\t', ''))
            # response.replace(body=bytes(''.join(htmls), encoding='utf-16'))
            body = bytes(''.join(htmls), encoding='utf-16')
        with open('处理后的response.html', 'wb') as f:
            # f.write(response.body)
            f.write(bytes(''.join(htmls), encoding='utf-16'))
        return HtmlResponse(url=request.url, status=200, body=body)

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
