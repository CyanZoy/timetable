# -*- coding: utf-8 -*-
"""
 @Time    : 2018/5/6 19:04
 @Author  : CyanZoy
 @File    : tete.py
 @Software: PyCharm
 """
import requests
payload = {'method': 'showPhoto', 'xh': '2016011280'}
url = 'http://10.70.3.104/xgxt/xsxx_xsgl.do?method=showPhoto'
headers = {'Cookie': 'JSESSIONID=4C022B73F453DBA10113DD6FF8E04212'}
r = requests.get(url, headers=headers,params=payload)
with open('2016012495.jpg', 'wb') as file:
    file.write(r.content)
