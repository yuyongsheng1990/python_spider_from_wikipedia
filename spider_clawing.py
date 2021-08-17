# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_wikipedia -> spider_clawing
# @Time: 2021/8/12 16:43 
# @Author: Yu Yongsheng
# @Description: 构建英文维基百科的python爬虫；用flask构建api接口

import pickle
import sys
import urllib
from cProfile import label

import bs4
import urllib3.util
from bs4 import BeautifulSoup
import re
import requests

# 爬虫程序
# 查询对象在wikipedia中的网址
def claw(url):
    # 访问、下载html网页

    # 请求头部，伪造浏览器，防止爬虫被反
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    response = urllib.request.urlopen(req, timeout=20)  # 发送请求，获得响应; 防止IncompleteRead()错误timeout=20
    text = response.read().decode('utf-8')  # 读取响应，获得文本
    # ----------------------------------------------------------------------------------------------------
    # 解析html网页
    soup = BeautifulSoup(text, 'html.parser')  # 创建soup对象，获取html源码
    # 获取html-main主内容便签部分
    soup_main = soup.find('div', class_=re.compile('mw-body-content')).find('div', class_='mw-parser-output')

    # 处理基本信息：过滤数据，去掉空白
    # 获取wiki中基本信息的标签块，它在标签<'table', class_='infobox biota'><'div', class_='toc'>中间
    infobox_tag = soup_main.select_one('table', class_=re.compile('infobox'))
    intro_text_list = []
    for br in infobox_tag.next_siblings:
        # print(br)
        if type(br) is bs4.element.Tag:  # 判断br是不是一个标签
            # 判断是否是栏目标题下的内容标签
            if br.name == 'p':
                intro_text_list.append(br.get_text())
            elif br.name == 'div' and ''.join(br.attrs['class']) == 'toc':
                break
    intro_after_filter = [re.sub('\n+', '', i) for i in intro_text_list]  # 去除换行
    # intro_after_filter = [''.join(i.split()) for i in intro_after_filter]  # 去除/0a乱码
    # 将字符串列表连成字符串并返回
    intro_after_filter = ''.join(intro_after_filter)
    # print(intro_after_filter)

    # 抽取信息框数据
    profile_dict = {}
    namelist = []
    valuelist = []
    profile_tag = infobox_tag.select('tr>td>span')
    for info in profile_tag:
        name = info.attrs['class'][0]
        namelist.append(str(name).capitalize())
        value = info.get_text()
        valuelist.append(value)

    for i, j in zip(namelist,
                    valuelist):  # 多遍历循环，zip()接受一系列可迭代对象作为参数，将对象中对应的元素打包成一个个tuple（元组），然后返回由这些tuples组成的list（列表）。
        profile_dict[i] = j
    # print(profile_dict)


    # 抽取人物履历信息、担任职位、人物经历等所有栏目信息v3.0
    catalog_tag = soup_main.find('div', class_=re.compile('toc$'))
    # print(catalog_tag)
    br_text_list = []
    # 目录tag后是人物履历等栏目
    for br in catalog_tag.next_siblings:
        # print(br)
        if type(br) is bs4.element.Tag:  # 判断br是不是一个标签
            # 判断是否是栏目标题下的内容标签
            if br.name == 'h2':  # 当出现栏目2级标题时，获取标题名称
                title_tag = br.find('span', class_=re.compile('headline'))
                title = title_tag.get_text()
                if re.match('See also|References', title):
                    return intro_after_filter, profile_dict, br_text_list
                # print(title)
                br_text_list.append('title-2: ' + title)
            elif br.name == 'h3':  # 当出现栏目3级标题时，获取标题名称
                title_tag = br.find('span', class_=re.compile('headline'))
                title = title_tag.get_text()
                # print(title)
                br_text_list.append('title-3: ' + title)
            elif br.name == 'h4':  # 当出现栏目4级标题时，获取标题名称
                title_tag = br.find('span', class_=re.compile('headline'))
                title = title_tag.get_text()
                # print(title)
                br_text_list.append('title-4: ' + title)
            elif br.name == 'p':  # 当出现文本内容的p标签时
                content = br.get_text()
                content = re.sub('\n+', '', content)
                # print(title)
                br_text_list.append(content)
    print(br_text_list)

    return intro_after_filter, profile_dict, br_text_list