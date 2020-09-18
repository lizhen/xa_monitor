#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'liz'

# @Time    : 2020/8/31
# @Author  : liz
# @FileName: analysis.py
# @Software: PyCharm

import numpy as np
from datetime import datetime
from tools.xlsx import Xlsx
from tools.las import Las
from tools.http import Http
import json
import logging as log

"""
需求：根据点云数据分析建筑物施工进度
功能：
1.分析建筑物施工进度；
2.读取配置文件；
"""

def execute():
    print('Start execution:', datetime.now())

    """加载配置文件"""
    building, path, ztjs = load_settings()

    INPUT_EXCEL = path['excel']['input']
    INPUT_LAS = path['las']['input']
    OUTPUT_EXCEL = path['excel']['output']

    AREA = building['area']
    MIN_HEIGHT = building['min_height']
    MAX_HEIGHT = building['max_height']
    THICKBESS = building['thickness']
    MULTIPOINT = building['multipoint']

    URL = ztjs['url']

    """建筑物信息处理"""
    xlsx = Xlsx()
    orig_buildings = xlsx.get_buildings(INPUT_EXCEL)
    if len(orig_buildings) == 0:
        print('There is no reference point.')
        return
    BLD_NUM = len(orig_buildings)
    buildings = sort_buildings(orig_buildings, AREA)

    """点云信息处理"""
    orig_las = Las(MIN_HEIGHT).get_las(INPUT_LAS)
    if len(orig_las) == 0:
        print('There is no point cloud.')
        return

    las = sort_las(orig_las)

    """建筑物与点云比较"""
    buildings_max = compare(buildings, las, BLD_NUM, MAX_HEIGHT)
    if len(orig_buildings) != len(buildings_max):
        log.error('The analysis result does not match the reality.')
        print('The analysis result does not match the reality.')
        return

    """建筑物施工进度"""
    buildings_pro = [[p[0], p[1], p[2], p[3], buildings_max[i], round((buildings_max[i]-p[3])/THICKBESS)] for i, p in enumerate(orig_buildings)]
    print("buildings process[1-5]:", buildings_pro[:5])
    xlsx.write_excel(str(OUTPUT_EXCEL).format(datetime.date(datetime.today())), buildings_pro, ['id', 'x', 'y', 'z', 'h', 'f'])

    print('Analysis of successful!')
    print('Stop execution:', datetime.now())

    """远端接口调用"""
    call_api = input('Do you want to continue making remote interface calls? Proceed (y/n) \n')
    if call_api.upper() == 'Y':
        buildings_json = json.loads([[p[0], p[5]] for p in buildings_pro])
        data = Http().post(URL, buildings_json)
        print('data:', data)
        return


def load_settings():
    """从配置文件中加载获取建筑物的相关信息"""
    import yaml
    data_file = open(r'.\\config\\building.yaml', 'r')
    settings = yaml.safe_load(data_file)
    data_file.close()
    return settings['building'], settings['path'], settings['ztjs']


def sort_buildings(orig_buildings, AREA):
    """X坐标与Y坐标先取整、拼接，再排序"""
    if len(orig_buildings) == 0:
        return orig_buildings

    buildings = [[int(data[0]), int(data[1]), int(data[2]), round(data[3])] for data in orig_buildings]
    print('orig_buildings[1-5]:', buildings[:5])
    buildings = [[x << 24 | y & 0xffff, p[0]] for p in buildings for x, y in [(p[1] - AREA, p[2] - AREA), (p[1] - AREA, p[2]), (p[1], p[2] - AREA), (p[1], p[2])]]
    print("new_buildings[1-5]:", buildings[:5])
    buildings = sorted(buildings, key=(lambda x: x[0]))
    print("sorted_buildings[1-5]:", buildings[:5])

    return buildings


def sort_las(orig_las):
    """X坐标与Y坐先拼接，再排序"""
    if len(orig_las) == 0:
        return orig_las

    print('orig_las[1-5]:', orig_las[:5])
    las = [[p[0] << 24 | p[1] & 0xffff, p[2]] for p in orig_las]
    print("new_las[1-5]:", las[:5])
    las = sorted(las, key=(lambda x: x[0]))
    print("sorted_las[1-5]:", las[:5])

    return las


def compare(buildings, las, BLD_NUM, MAX_HEIGHT):
    cnt_bld = np.zeros((BLD_NUM, MAX_HEIGHT))
    ptr_las, len_las = 0, len(las) - 1
    ptr_bld, len_bld = 0, len(buildings) - 1
    try:
        while ptr_las < len_las and ptr_bld < len_bld:
            while ptr_las < len_las and ptr_bld < len_bld and las[ptr_las][0] > buildings[ptr_bld][0]:
                ptr_bld += 1
            while ptr_las < len_las and ptr_bld < len_bld and las[ptr_las][0] < buildings[ptr_bld][0]:
                ptr_las += 1
            while ptr_las < len_las and ptr_bld < len_bld and las[ptr_las][0] == buildings[ptr_bld][0]:
                if las[ptr_las][1] < MAX_HEIGHT:
                    cnt_bld[buildings[ptr_bld][1]][las[ptr_las][1]] += 1
                ptr_las += 1
    except Exception as e:
        log.error('Error executing building and point cloud match.')
        print('Error executing building and point cloud match，Error cause：%s' % e)
        return []

    max_bld = np.argmax(cnt_bld, axis=1) / 50
    print('Analysis height buildings[1-10]:', max_bld)

    return max_bld


if __name__ == '__main__':
    execute()
