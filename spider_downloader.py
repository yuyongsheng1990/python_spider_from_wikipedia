# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_wikipedia -> spider_downloader
# @Time: 2021/8/12 16:44 
# @Author: Yu Yongsheng
# @Description: 构建英文维基百科的python爬虫

import os
import re
from urllib.error import HTTPError

import requests
import xlrd
import xlwt
from xlutils.copy import copy
import json


# 下载爬到的数据：基本信息、信息框、图片
def download(name, intro, profile_dict, br_text_list):
    project_path = os.getcwd()
    # print('project_path:' + project_path)

    # 保存百科基本信息
    # if not os.path.exists('introduction'):
    #     os.mkdir('introduction')
    # introduction_file = project_path + '/introduction/' + name + '.json'
    # print(introduction_file)
    # with open(introduction_file, 'w', encoding='utf-8') as f:
        # 转换成json格式输出
    intro_dict = {'intro': intro}
        # 防止json编码时中文ascii乱码，用ensure_ascii=False
        # intro_dict_json = json.dumps(intro_dict, indent=4, ensure_ascii=False)

        # f.write(intro_dict_json + '\n')
    # print('introduction输出完毕')

    # 将信息框数据以json格式输出
    # with open(introduction_file, 'a+') as f:
        # profile_dict_json = json.dumps(profile_dict, indent=4, ensure_ascii=False, sort_keys=False)
        # f.write(profile_dict_json + '\n')


    # 保存人物履历、职务、研究等栏目内容到基本信息.txt中
    # api返回json数据，在web中进行展示
    cv_output = {}
    # with open(introduction_file, 'a+') as f:
    # print(br_text_list)
    # 转换成json格式输出
    key_2 = ''
    value = ''
    key_3 = ''
    key_4 = ''
    output_dict_2 = {}
    output_dict_3 = {}
    output_dict_4 = {}
    for i in range(len(br_text_list)):
        # print(i)
        item = br_text_list[i]
        if isinstance(item, str):
            # 2级标题
            if item.startswith('title-2'):
                key_2 = item.split(': ')[1]
                # continue
            # 3级标题
            elif item.startswith('title-3'):
                key_3 = item.split(': ')[1]
                # continue
            elif item.startswith('title-4'):
                key_4 = item.split(': ')[1]
            else:
                value += item

            # 对下一索引值进行判断，它是h2，h3，h4还是text文本
            if i+1 < len(br_text_list):
                # 如果后面跟着h4标题
                if br_text_list[i+1].startswith('title-4'):
                    # 如果h4后面跟着h4标题
                    if key_4:
                        output_dict_4.update({key_4: value})
                        key_4 = ''
                        value = ''
                        continue
                    # 如果h3+text，后面跟h4标题时，
                    elif key_3 and value:
                        output_dict_4.update({'': value})
                        value = ''
                        continue
                # 如果后面跟着h3标题
                elif br_text_list[i+1].startswith('title-3'):
                    # 如果h4后面跟着h3标题
                    if key_4:
                        output_dict_4.update({key_4: value})
                        key_4 = ''
                        value = ''
                        output_dict_3.update({key_3: output_dict_4})
                        key_3 = ''
                        output_dict_4 = {}
                        continue
                    # 如果h3后面跟h3标题
                    if key_3:
                        output_dict_3.update({key_3: value})
                        key_3 = ''
                        value = ''
                    # 如果h2+text，后面跟h3标题时，
                    elif key_2 and value:
                        output_dict_text = {'': value}
                        output_dict_3.update(output_dict_text)
                        # output_dict_2_json = json.dumps(output_dict_2, indent=4, ensure_ascii=False)
                        # f.write(output_dict_2_json + '\n')
                        value = ''
                        continue
                # 如果后面跟着h2标题
                elif br_text_list[i+1].startswith('title-2'):
                    # 如果h4后面跟着h2标题
                    if key_4:
                        output_dict_4.update({key_4: value})
                        key_4 = ''
                        value = ''
                        output_dict_3.update({key_3: output_dict_4})
                        key_3 = ''
                        output_dict_4 = {}
                        output_dict_2.update({key_2: output_dict_3})
                        key_2 = ''
                        output_dict_3 = {}
                    # 如果h3后面跟h2标题
                    if key_3:
                        output_dict_3.update({key_3: value})
                        output_dict_2 = {key_2: output_dict_3}
                        cv_output.update(output_dict_2)
                        # output_dict_2_json = json.dumps(output_dict_2, indent=4, ensure_ascii=False)
                        # f.write(output_dict_2_json + '\n')
                        key_2 = ''
                        key_3 = ''
                        value = ''
                        output_dict_2 = {}
                        output_dict_3 = {}
                        continue
                    # 如果h2后面跟h2标题
                    else:
                        output_dict_2 = {key_2: value}
                        cv_output.update(output_dict_2)
                        # output_dict_2_json = json.dumps(output_dict_2, indent=4, ensure_ascii=False)
                        # f.write(output_dict_2_json + '\n')
                        value = ''
                        output_dict_2 = {}
                        continue
                else:
                    continue
            else:
                if str(br_text_list[-1]).startswith('title'):
                    value = ''
                # 当最后是以h4标题+/-文本结尾时
                if key_4:
                    output_dict_4.update({key_4: value})
                    key_4 = ''
                    value = ''
                    output_dict_3.update({key_3: output_dict_4})
                    key_3 = ''
                    output_dict_4 = {}
                    output_dict_2.update({key_2: output_dict_3})
                    key_2 = ''
                    output_dict_3 = {}
                # 当最后是以h3标题+/-文本结尾时
                if key_3:
                    output_dict_3.update({key_3: value})
                    key_3 = ''
                    value = ''
                    output_dict_2.update({key_2: output_dict_3})
                    key_2 = ''
                    output_dict_3 = {}
                # 当最后是以h2标题+/-文本结尾时
                if key_2:
                    output_dict_2 = {key_2: value}
                cv_output.update(output_dict_2)
                # output_dict_2_json = json.dumps(output_dict_2, indent=4, ensure_ascii=False)
                # f.write(output_dict_2_json + '\n')
        # 输出字典格式的图书信息
        elif isinstance(item, list):
            cv_output.update({key_2: item})
            # output = json.dumps({key_2: item}, indent=4, ensure_ascii=False)
            # f.write(output)
            continue
    print('人物履历输出完毕')

    '''
    # 保存图片
    # 请求头部，伪造浏览器，防止爬虫被反
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    download_limit = 10  # 单个人物下载的最大图片数
    if not os.path.exists('img'):
        os.mkdir('img')
    name_path = project_path + '/img/' + name
    if not os.path.exists(name_path):
        os.mkdir(name_path)

    count = 1
    for img_url in img_list:
        try:
            response = requests.get(img_url, headers=headers)  # 得到访问的网址
            content = response.content
            filename = name_path + '/' + name + '_%s.png' % count
            with open(filename, "wb") as f:
                # 如果图片质量太差，跳过
                if len(content) < 1000:
                    continue
                f.write(content)  # 保存图片
            response.close()
            count += 1
            # 每个模特最多只下载download_limit张
            if count > download_limit:
                break

        except HTTPError as e:  # HTTP响应异常处理
            print(e.reason)
    '''
    return intro_dict, profile_dict, cv_output
