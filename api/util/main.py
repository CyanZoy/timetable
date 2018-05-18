# -*- coding: utf-8 -*-
"""
 @Time    : 2018/5/6 14:29
 @Author  : CyanZoy
 @File    : main.py
 @Software: PyCharm
 """
import hashlib


def equal_sign(sortlist, sign):
    sortlist.sort()
    sha = hashlib.sha1()
    sha.update(''.join(sortlist).encode('utf-8'))
    print(sha.hexdigest(), sign)
    if sha.hexdigest() == sign:
        return True
    else:
        return False