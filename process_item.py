#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import redis
import json
import os

def process_item():
    # 创建redis数据库连接
    rediscli = redis.Redis(host = "127.0.0.1", port = 6379, db = "0")

    while True:
        # redis 数据表名 和 数据
        source, data = rediscli.blpop("sinanews:items")

        # 将json对象转换为Python对象
        data = json.loads(data)

        article_url = data['article_url']
        path = data['subpath']

        # 如果目录不存在则创建目录
        if not os.path.exists(path):
            os.makedirs(path)

        # 文件名为子链接url中间部分，并将 / 替换为 _，保存为 .txt格式
        filename = article_url[7:-6].replace('/','_')
        filename += ".txt"

        with open(data['subpath'] + '/' + filename, 'wb') as f:
            try:
                f.write(data['article_title'].encode())
                f.write(data['article_url'].encode())
                f.write(data['article_content'].encode())
            except:
                pass


if __name__ == "__main__":
    process_item()
