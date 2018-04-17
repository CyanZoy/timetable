# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/7 15:45
 @Author  : CyanZoy
 @File    : urls.py
 @Software: PyCharm
 """
from django.urls import path, re_path
from scheduler import views

urlpatterns = [
    path('', views.index),
    re_path('index', views.index),
    path('table', views.table),
    path('Te', views.Te),
]
