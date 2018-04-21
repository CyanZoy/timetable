# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/15 16:38
 @Author  : CyanZoy
 @File    : main.py
 @Software: PyCharm
 @Describe: 数据
 """
from django.db.utils import DatabaseError
import math
# Changelist settings
ALL_VAR = 'all'
ORDER_VAR = 'o'
ORDER_TYPE_VAR = 'ot'
PAGE_VAR = 'p'
SEARCH_VAR = 'q'
ERROR_FLAG = 'e'

# IGNORED_PARAMS = (
#     ALL_VAR, ORDER_VAR, ORDER_TYPE_VAR, SEARCH_VAR, IS_POPUP_VAR, TO_FIELD_VAR)


class ChangeList:
    """
        list_per_page:每页的数据数量
        page:数据库交互
    """
    def __init__(self, model, list_per_page, *args, **kwargs):
        self.model = model
        self.list_per_page = list_per_page
        self.count = self.model.objects.all().count()
        self.args = args
        self.kwargs = kwargs
        self.key_isnull = self.model.objects.filter(**kwargs).count()

    def get_results(self):
        result = self.model.objects.all()[:self.list_per_page]
        return result

    def get_results_by_page(self, page, *args, **kwargs):
        """查询指定页数内的数据,kwargs为过滤参数"""
        self.page = page
        try:
            result = self.model.objects.filter(*args, **kwargs)[(page-1)*self.list_per_page:
                                                (page-1)*self.list_per_page+self.list_per_page]
            return result
        except DatabaseError as e:
            print(e, '->', 'ChangList.get_results_by_page')

    def get_result_by_range(self, *args):
        result = self.model.objects.filter(**self.kwargs).order_by(*args)[:self.list_per_page].values()
        return result


class Pagina:
    """分页"""
    def __init__(self, model, page, list_per_page, *args, **kwargs):
        self.model = model
        self.page = page
        self.has_previous = False
        self.has_next = False
        self.count = False
        self.left_page = [1, 2, 3]
        self.mid_page = []
        self.right_page = []
        self.list_per_page = list_per_page
        self.result = self.get_result(self.page, *args, **kwargs)

    def get_result(self, page, *args, **kwargs):
        """根据指定页数"""
        try:
            self.s = ChangeList(self.model, self.list_per_page, *args, **kwargs)
        except:
            pass

        self.count = self.s.key_isnull

        all_page = int(math.ceil(self.count / self.list_per_page))

        if page > 1:
            self.has_previous = page - 1

        if page < all_page:
            self.has_next = page + 1

        k = all_page
        for _ in range(3):
            self.right_page.append(k)
            k -= 1

        if page in [3, 4]:
            self.mid_page = ['4', '5', '6']
        elif page == all_page-2:
            self.right_page.append(page - 1)

        elif page not in self.left_page and page not in self.right_page:
            self.mid_page.append(page)
            if page - 1 not in self.left_page:
                self.mid_page.append(page - 1)
            if page + 1 not in self.right_page:
                self.mid_page.append(page + 1)
            elif page - 2 not in self.left_page:
                self.mid_page.append(page - 2)

        return self.s.get_results_by_page(page, *args, **kwargs)
