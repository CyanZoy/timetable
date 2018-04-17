# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/16 15:54
 @Author  : CyanZoy
 @File    : pagetag.py
 @Software: PyCharm
 @Describe: 分页
 """
from django import template
from django.utils.html import format_html

register = template.Library()

__Author = 'CyanZoy'


@register.simple_tag
def circle_page():
    pass
