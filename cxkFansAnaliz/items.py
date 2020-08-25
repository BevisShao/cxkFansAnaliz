# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class CxkfansanalizItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 粉丝的名称
    name = Field()
    # ID
    id = Field()
    # 性别
    gender = Field()
    # 个人空间背景样式
    background_style = Field()
    # 关注的数量
    follow_num = Field()
    # 粉丝的数量
    fans_num = Field()
    # 粉丝的粉丝列表
    fans_lists_url = Field()
    # 个人动态数量
    article_num = Field()
    # 个人等级
    level = Field()
    # 位置
    location = Field()
    # 星座
    constellation = Field()
    # 生日
    birthday = Field()
    # 会员等级  -1为非会员
    vip_level = Field()
    # 个人简介
    summary = Field()
    # 关注的方式
    way_of_fans =Field()
    # 关注人员的列表
    follow_list = Field()
    # 个人头像url
    picture_url = Field()
    # 个人头像文本
    picture_base64 = Field()
