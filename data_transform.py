# -*- coding:utf-8 -*-


import re

# 进制转换

# 预处理，处理值、单位及其大小写等问题
def preTrans(target):
    units = ['b', 'k', 'm', 'g', 't']
    # 将数值与单位拆分
    tmp = re.findall(r'[0-9]+|[a-zA-Z]+',target)
    # print(tmp)
    if len(tmp) > 2:
        print("Not a vaild value")
    amt = tmp[0]
    unit = tmp[1]
    if len(unit) == 2 and unit[1].lower() == 'b':
        unit = unit[0]
    elif len(unit) > 2:
        print("Not a vaild value")
    
    if unit.lower() not in units:
        print("Not a vaild value")
    
    idx = units.index(unit.lower())

    return (int(amt), units[idx+1], idx)

# 小进大，如 k 到 m
def transfromer1(target):
    i, unit, idx = preTrans(target)
    
    cnt = 0
    while (i >= 1024):
        i /= 1024
        cnt += 1

    return (str(i)+unit)
    

# 反向转换，如 m 到 b
def transfromer2(target):
    res, unit, idx = preTrans(target)
    while(idx > 0):
        res *= 1024
        idx -= 1
    return(res)
    


# 日期转换

import time

# 时间字符串转时间戳
def dateStr2Timestamp(date_str):
    timeArray = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)

    return timestamp

# 时间戳转日期字符串
def timestamp2DateStr(timestamp):
    time_local = time.localtime(timestamp)
    date_str = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

    return date_str


# 测试代码
if __name__ == '__main__':
    print(transfromer1('2050K'))
    print(transfromer2('100m'))
    print(dateStr2Timestamp('2018-7-02 10:58:12'))
    print(timestamp2DateStr(1530525333))