# -*- coding: utf-8 -*-
import scrapy
import os
from sina.items import SinaItem


class SinanewsSpider(scrapy.Spider):
    name = 'sinanews'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []

        # 拿到大类的标题及链接
        parent_titles = response.xpath("//div[@id='tab01']//h3/a/text()").extract()
        parent_urls = response.xpath("//div[@id='tab01']//h3/a/@href").extract()

        # 小类的标题及链接
        subtitles = response.xpath("//div[@id='tab01']/div/ul/li/a/text()").extract()
        suburls = response.xpath("//div[@id='tab01']/div/ul/li/a/@href").extract()


        # 爬取所有大类
        for i in range(len(parent_titles)):
            # 指定大类目录所在的路径及目录名
            parent_filename = './Data/' + parent_titles[i]

            # 如果目录不存在则创建目录
            if not os.path.exists(parent_filename):
                os.makedirs(parent_filename)

            # 爬取所有小类
            for j in range(len(subtitles)):
                item = SinaItem()

                # 保存大类的标题和链接
                item['parent_title'] = parent_titles[i]
                item['parent_url'] = parent_urls[i]

                # 判断小类是否是该大类的下的小类
                is_belong = suburls[j].startswith(item['parent_url'])


                # 
                if is_belong:

                    sub_filename = parent_filename + '/' + subtitles[j]

                    # 如果目录不存在则创建目录
                    if not os.path.exists(sub_filename):
                        os.makedirs(sub_filename)

                    # 保存子类的标题和链接
                    item['subtitle'] = subtitles[j]
                    item['suburl'] = suburls[j]

                    item['subpath'] = sub_filename

                    items.append(item)

        for item in items:
            yield scrapy.Request(item['suburl'], meta={'meta_1':item}, callback=self.parse_links)

    def parse_links(self, response):
        # 拿到传入的 item 信息
        meta_1 = response.meta['meta_1']

        # 页面中所有的链接
        links = response.xpath("//a/@href").extract()

        items = []

        # 处理所有的链接
        for link in links:
            # 判断该链接是否是大类下的链接，且是 .shtml 结尾
            is_ok = link.startswith(meta_1['parent_url']) and link.endswith('.shtml')

            # 
            if is_ok:
                item = SinaItem()
                item['parent_url'] = meta_1['parent_url']
                item['parent_title'] = meta_1['parent_title']
                item['subtitle'] = meta_1['subtitle']
                item['suburl'] = meta_1['suburl']
                item['subpath'] = meta_1['subpath']
                item['article_url'] = link

                items.append(item)

        for i in items:
            yield scrapy.Request(i['article_url'], meta={'meta_2':item}, callback=self.parse_info)


    def parse_info(self, response):
        # 拿到传入的 item 信息
        meta_2 = response.meta['meta_2']

        item = SinaItem()
        item['article_url'] = response.url
        item['article_title'] = response.xpath('//h1/text()').extract_first()

        content = response.xpath("//div[@id='artibody']/p/text()").extract()
        item['article_content'] = ''.join(content).replace(' ', '').replace('\u3000','')
        item['parent_title'] = meta_2['parent_title']
        item['parent_url'] = meta_2['parent_url']
        item['subtitle'] = meta_2['subtitle']
        item['suburl'] = meta_2['suburl']
        item['subpath'] = meta_2['subpath']

        yield item

