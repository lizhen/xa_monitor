#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'liz'

# @Time    : 2020/8/31
# @Author  : liz
# @FileName: xlsx.py
# @Software: PyCharm

import pandas as pd
import logging

"""
需求：Excel读写
功能：
1.获取已知建筑坐标；
2.读、写Excel；
"""


class Xlsx(object):

    def __init__(self):
        pass

    def get_buildings(self, fpath):
        """获取已知建筑坐标"""
        return self.read_excel(fpath)

    def get_buildings_bak(self, fpath):
        """获取已知建筑坐标"""
        datas = self.read_excel(fpath)

        buildings = [[int(data[0]), int(data[1]), int(data[2]), round(data[3])] for data in datas]

        return buildings

    def read_excel(self, fpath):
        """读取Excel"""
        if fpath.strip() == '':
            print('File path cannot be empty.')
            return []

        try:
            df = pd.read_excel(fpath)
            return df.to_numpy()
        except Exception as e:
            logging.error('加载Excel出错，出错原因：%s' % e)
            print('加载Excel出错，出错原因：%s' % e)
            return []

    def write_excel(self, fpath, datas, columns=['id', 'code', 'x', 'y', 'z']):
        """写入Excel"""
        if fpath.strip() == '':
            print('File path cannot be empty.')
            return

        if len(datas) == 0:
            print('Datas cannot be empty.')
            return

        df = pd.DataFrame(datas, columns=columns)
        df.to_excel(fpath, index=False)
