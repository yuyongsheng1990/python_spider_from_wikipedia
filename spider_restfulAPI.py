# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_wikipedia -> spider_restfulAPI
# @Time: 2021/8/12 16:45 
# @Author: Yu Yongsheng
# @Description: 构建英文维基百科的python爬虫

import json
import re

import requests

import spider_clawing
import spider_downloader

import urllib
from urllib.error import HTTPError
from bs4 import BeautifulSoup

# 安装Restful package
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource


# 防止ssl报错
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 初始化app, api
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/<name>')
def home(name):

    # 去除favicon.ico干扰
    if name =="favicon.ico":
        pass
    else:
        # 判断百度百科上是否存在这个人的页面，或该人名页面是否需要人工跳转
        # 访问、下载html网页
        url = 'https://en.wikipedia.beta.wmflabs.org/wiki/' + name  # 请求地址
        # 请求头部，伪造浏览器，防止爬虫被反
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        # 利用请求地址和请求头部构造请求对象
        try:
            req = urllib.request.Request(url=url, headers=headers, method='GET')
            response = urllib.request.urlopen(req, timeout=20)  # 发送请求，获得响应; 防止IncompleteRead()错误timeout=20
        except HTTPError as e:
            # 检查该页面是否存在
            if e.code == 404:
                return "The page you searched does not exist, please check the name"

        intro, profile_dict, br_text_list = spider_clawing.claw(url)
        intro_dict, profile_dict, cv_output = spider_downloader.download(name, intro, profile_dict, br_text_list)
        output = [intro_dict, profile_dict, cv_output]
        # print(output)
        intro_dict_json = json.dumps(output, indent=4)
        return intro_dict_json


if __name__ == '__main__':
    # 设置ip、端口
    app.run(host='192.168.0.101', port=8891)
    # 启动api接口
    # app.run()
