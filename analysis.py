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

    building, path, ztjs = load_settings()

    INPUT_EXCEL = path['excel']['input']
    INPUT_LAS = path['las']['input']
    OUTPUT_EXCEL = path['excel']['output']

    AREA = building['area']
    MIN_HEIGHT = building['min_height']
    MAX_HEIGHT = building['max_height']
    THICKBESS = building['thickness']

    URL = ztjs['url']

    xlsx = Xlsx()
    orig_buildings = xlsx.get_buildings(INPUT_EXCEL)
    if len(orig_buildings) == 0:
        print('There is no reference point.')
        return
    print('orig_buildings[1-5]:', orig_buildings[:5])

    orig_las = Las(MIN_HEIGHT).get_las(INPUT_LAS)
    if len(orig_las) == 0:
        print('There is no point cloud.')
        return
    print('orig_las[1-5]:', orig_las[:5])

    buildings = [[x << 24 | y & 0xffff, p[0]] for p in orig_buildings for x, y in [(p[1] - AREA, p[2] - AREA), (p[1] - AREA, p[2]), (p[1], p[2] - AREA), (p[1], p[2])]]
    print("buildings[1-5]:", buildings[:5])
    buildings = sorted(buildings, key=(lambda x : x[0]))
    print("sorted buildings[1-5]:", buildings[:5])

    las = [[p[0] << 24 | p[1] & 0xffff, p[2]] for p in orig_las]
    print("las[1-5]:", las[:5])
    las = sorted(las, key=(lambda x : x[0]))
    print("sorted las[1-5]:", las[:5])

    cnt_bld = np.zeros((len(orig_buildings), MAX_HEIGHT))
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
        return

    max_bld = np.argmax(cnt_bld, axis=1)
    max_bld = max_bld / 50
    print('Analysis height buildings[1-10]:', max_bld)

    if len(orig_buildings) != len(max_bld):
        log.error('The analysis result does not match the reality.')
        print('The analysis result does not match the reality.')
        return

    buildings_pro = [[p[0], p[1], p[2], p[3], max_bld[i], round((max_bld[i]-p[3])/THICKBESS)] for i, p in enumerate(orig_buildings)]
    print("buildings process[1-5]:", buildings_pro[:5])
    xlsx.write_excel(str(OUTPUT_EXCEL).format(datetime.date(datetime.today())), buildings_pro, ['id', 'x', 'y', 'z', 'h', 'f'])

    print('Analysis of successful!')
    print('Stop execution:', datetime.now())

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


if __name__ == '__main__':
    execute()
