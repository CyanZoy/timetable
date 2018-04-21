# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/18 9:45
 @Author  : CyanZoy
 @File    : date_format.py
 @Software: PyCharm
 """


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj