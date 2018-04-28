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
    path('login/', views.Te2),
    re_path('index', views.index),
    path('table', views.table),
    re_path('specific', views.specific),
    path('Te', views.Te),
]
