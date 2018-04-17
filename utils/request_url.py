# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/13 17:09
 @Author  : CyanZoy
 @File    : request_url.py
 @Software: PyCharm
 """


def divice_request_path(request, defaut_div='/'):
    p = []
    path = request.path
    if path:
        for _ in path.split(defaut_div):
            p.append(_)
    return p
