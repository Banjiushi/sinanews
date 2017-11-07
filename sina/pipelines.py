# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

class SinaPipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item
    # def process_item(self, item, spider):
    #     article_url = item['article_url']

    #     # 文件名为子链接url中间部分，并将 / 替换为 _，保存为 .txt格式
    #     filename = article_url[7:-6].replace('/','_')
    #     filename += ".txt"

    #     with open(item['subpath'] + '/' + filename, 'wb') as f:
    #         f.write(item['article_title'].encode())
    #         f.write(item['article_url'].encode())
    #         f.write(item['article_content'].encode())

    #     return item