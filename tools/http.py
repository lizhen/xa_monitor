#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'liz'

# @Time    : 2020/8/31
# @Author  : liz
# @FileName: http.py
# @Software: PyCharm

import requests, json
import logging

"""
需求：请求网络资源
功能：
1.发送Get、Post请求；
"""


class Http(object):

    def __init__(self):
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:51.0) Gecko/20100101 Firefox/51.0"}

    def get(self, url):
        """Get消息"""
        try:
            r = requests.get(url, headers=self.headers)
            r.encoding = 'UTF-8'
            json_response = json.loads(r.text)
            return json_response
        except Exception as e:
            logging.error('get请求出错，出错原因：%s' % e)
            print('get请求出错，出错原因：%s' % e)
            return {}

    def post(self, url, params):
        """POST消息"""
        data = json.dumps(params)
        try:
            r = requests.post(url, data=data, headers=self.headers)
            json_response = json.loads(r.text)
            return json_response
        except Exception as e:
            logging.error('post请求出错，出错原因：%s' % e)
            print('post请求出错，出错原因：%s' % e)
            return {}
