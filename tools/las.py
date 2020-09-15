#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'liz'

# @Time    : 2020/8/31
# @Author  : liz
# @FileName: las.py
# @Software: PyCharm

import os
import pylas
import logging

"""
需求：加载点云
功能：
1.获取点云；
"""


class Las(object):

    def __init__(self, elevation):
        self.__elevation = elevation

    def get_las(self, fpath):
        """获取点云"""

        files = self.get_las_path(fpath)
        if len(files) == 0:
            print('No LAS file was found under current path.')
            return []

        las = []
        for file in files:
            data = self.read_las(file)

            lx, ly, lz = data.x, data.y, data.z

            las += [[int(lx[i]), int(ly[i]), int(round(lz[i]*10*5))] for i in range(len(data.points))]

        return las

    def read_las(self, fpath):
        """读取点云"""
        if fpath.strip() == '':
            print('File path cannot be empty.')

        try:
            with pylas.open(fpath) as fh:
                print('Date from Header:', fh.header.date)
                print('Software from Header:', fh.header.generating_software)
                print('Points from Header:', fh.header.point_count)

                las = fh.read()
            return las
        except Exception as e:
            logging.error('加载Las出错，出错原因：%s' % e)
            print('加载Las出错，出错原因：%s' % e)
            return []

    def get_las_path(self, fpath):
        """获取目录下所有las文件路径"""
        if not os.path.exists(fpath):
            print('File or directory does not exist.')
            return []

        if os.path.isfile(fpath):
            if not os.path.splitext(fpath)[1] == '.las':
                return []

            return [fpath]
        elif os.path.isdir(fpath):
            return [os.path.join(root, file) for root, dirs, files in os.walk(fpath) for file in files if os.path.splitext(file)[1] == '.las']
        else:
            return []