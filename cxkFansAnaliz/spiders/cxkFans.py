# -*- coding: utf-8 -*-
import scrapy
import scrapy_redis
import logging
from scrapy import selector
from cxkFansAnaliz.items import CxkfansanalizItem
from scrapy.http import Request
from urllib.parse import quote
import re
from cxkFansAnaliz.settings import DOMAIN_HOST


class CxkfansSpider(scrapy.Spider):
    name = 'cxkFans'
    allowed_domains = ['weibo.com']
    # https://weibo.com/p/1003061776448504/follow?relate=fans&page=1#Pl_Official_HisRelation__58
    base_url = 'https://weibo.com/p/1003061776448504/follow?relate=fans&page={}#Pl_Official_HisRelation__58'
    start_urls = [base_url.format(1)]

    # 此链接贴到谷歌浏览器里出现跳转到首页的现象，应该是需要登陆才能访问，所以需要传送个cookies

    def parse(self, response):
        response_code = response.status
        if response_code == 200:
            # print('response_code:', response_code)
            # print(response.text)
            with open('fanslists.html', 'w', encoding='utf-16') as f:
                f.write(response.text)
            # lists = response.xpath('//ul[@class="follow_list"]/li').extract()
            lists = response.selector.xpath('//div/ul/li[contains(@class,"S_line2") and contains(@action-type,"itemClick")]')
            # print(lists, '-----------------sssssss')
            for li in lists:
                item = CxkfansanalizItem()
                item['name'] = li.xpath('.//dd/div/a[@class="S_txt1"]/text()').extract_first()
                # ID
                ID_text = li.xpath('.//dd/div/a[@class="S_txt1"]/@usercard').extract_first()
                re_result = re.search('id=(\d+?)&.*', ID_text)
                item['id'] = re_result.group(1)
                # 性别
                gender_text = li.xpath('.//dd/div/a/i/@class').extract_first()
                item['gender'] = 'male' if 'icon_male' in gender_text else 'female'
                # 个人空间背景样式
                item['background_style'] = 'default'
                # 关注的数量
                item['follow_num'] = li.xpath('.//div[@class="info_connect"]/span[1]/em/a/text()').extract_first()
                # 粉丝的数量
                item['fans_num'] = li.xpath('.//div[@class="info_connect"]/span[2]/em/a/text()').extract_first()
                # 粉丝列表
                item['fans_lists_url'] = li.xpath('.//div[@class="info_connect"]/span[2]/em/a/@href').extract_first()
                # 个人动态数量
                item['article_num'] = li.xpath('.//div[@class="info_connect"]/span[3]/em/a/text()').extract_first()
                # 个人等级
                item['level'] = 'default'
                # 位置
                item['location'] = li.xpath('.//dd/div[@class="info_add"]/span/text()').extract_first()
                # 星座
                item['constellation'] = 'default'
                # 生日
                item['birthday'] = 'default'
                # 会员等级  -1为非会员
                vip_text = li.xpath('.//dd/div/a/em/@class').extract_first()
                re_result_vip = re.search('.*icon_member(\d+?)', vip_text, re.S) if vip_text else 0
                item['vip_level'] = re_result_vip.group(1) if vip_text else 0
                # 个人简介
                item['summary'] = li.xpath('.//dd/div[@class="info_intro"]/span/text()').extract_first()
                # 关注的方式
                item['way_of_fans'] = li.xpath('.//dd/div[@class="info_from"]/a[@class="from"]/text()').extract_first()
                # 关注人员的列表
                # follow_list = scrapy.Field()
                # 个人头像url
                item['picture_url'] = li.xpath('.//dl/dt/a/img/@src').extract_first()
                # 个人头像文本
                item['picture_base64'] = 'default'
                # infromation = ','.join(item.values())
                # print('单个用户个人信息：{}'.format(infromation))
                # print('单个用户个人信息：{}'.format(item))
                yield Request(url='https://weibo.com/{}/info'.format(item['id']),
                              callback=self.parse_fans_space, meta={'item': item})
                for i in range(1, 6):
                    yield Request(url=DOMAIN_HOST+'/p/100505' + item['id'] + '/follow?relate=fans&page={}#Pl_Official_HisRelation__59'.format(i), callback=self.parse, dont_filter=False)
        elif response_code == 404 or response_code == 504:
            print('网页404')
        elif response_code == 503:
            print('网页503，请求频繁')
        else:
            print('其他状态码')
        urls = [self.base_url.format(i) for i in range(2, 7)]
        for url in urls:
            yield Request(callback=self.parse, url=url)

    def parse_fans_space(self, response):
        item = response.meta['item']
        lists = response.xpath('//div[@class="WB_innerwrap"]//ul[@class="clearfix"]/li')
        details = {}
        for li in lists:
            keys_text = li.xpath('.//span[1]/text()').extract_first()
            values_text = li.xpath('.//span[2]/text()').extract_first()
            details[keys_text] = values_text
        # 个人空间背景样式  http://img.t.sinajs.cn/t5/skin/public/profile_cover/035.jpg
        backgroud_node = response.xpath('//div[@class="PCD_header"]/div[@class="pf_wrap"]/div[1]/@style').extract_first()
        re_background_url = re.search('.*?\((.*?)\)', backgroud_node, re.S)
        item['background_style'] = re_background_url.group(1) if re_background_url else '未获取'
        # 个人等级
        item['level'] = 'default'
        # 星座
        item['constellation'] = 'default'
        # 生日
        item['birthday'] = details.get('生日：')
        # 个人头像文本
        item['picture_base64'] = 'default'
        # print('单个用户个人信息：{}'.format(item))
        yield item
