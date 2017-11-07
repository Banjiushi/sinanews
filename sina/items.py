# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 大类的标题
    parent_title = scrapy.Field()
    # 大类的链接
    parent_url = scrapy.Field()

    # 小类的标题
    subtitle = scrapy.Field()
    # 小类的链接
    suburl = scrapy.Field()
    # 保存子类路径，在后边存储数据时使用
    subpath = scrapy.Field()

    # 文章的标题
    article_title = scrapy.Field()
    # 文章的链接
    article_url = scrapy.Field()
    # 文章的内容
    article_content = scrapy.Field()

