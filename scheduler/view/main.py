# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/15 16:38
 @Author  : CyanZoy
 @File    : main.py
 @Software: PyCharm
 @Describe: 数据
 """
from django.db.utils import DatabaseError
from scheduler.models import *
from django.db.models import Q
import math
from utils.date_format import date_handler, DateFormat
from collections import defaultdict
# Changelist settings
ALL_VAR = 'all'
ORDER_VAR = 'o'
ORDER_TYPE_VAR = 'ot'
PAGE_VAR = 'p'
SEARCH_VAR = 'q'
ERROR_FLAG = 'e'


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
        self.key_isnull = self.model.objects.filter(*args, **kwargs).count()

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

    def get_result_by_range(self, *args, **kwargs):
        """获取指定条数的数据，和传入自定的排序规则"""
        result = self.model.objects.filter(**kwargs).order_by(*args)[:self.list_per_page]
        return result

    @staticmethod
    def get_field_count(model, key):
        """获取某个字段的最值的object"""
        return model.objects.latest(key)


class Pagina:
    """分页"""
    def __init__(self, model, page, list_per_page, *args, **kwargs):
        self.model = model
        self.page = page
        self.has_previous = False
        self.has_next = False
        self.count = False
        self.left_page = []
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

        if all_page > 3:
            self.left_page = [1, 2, 3]
            k = all_page
            for _ in range(3):
                self.right_page.append(k)
                k -= 1
            if page in [3, 4]:
                self.mid_page = [i for i in range(1, all_page+1) if i in range(4, 7)]
            elif page == all_page - 2 and all_page > 4:
                self.right_page.append(page - 1)
        else:
            self.left_page = [i for i in range(1, all_page+1)]

        if page > 1:
            self.has_previous = page - 1

        if page < all_page:
            self.has_next = page + 1

        elif page not in self.left_page and page not in self.right_page:
            self.mid_page.append(page)
            if page - 1 not in self.left_page:
                self.mid_page.append(page - 1)
            if page + 1 not in self.right_page:
                self.mid_page.append(page + 1)
            elif page - 2 not in self.left_page:
                self.mid_page.append(page - 2)
        return self.s.get_results_by_page(page, *args, **kwargs)


class JsData:
    def __init__(self, num, name=None):
        self.num = num
        self.name = name

    def select_by_name(self, name):
        """根据姓名查找"""
        pass

    def select_by_number(self, number):
        """根据教师职工号查找"""
        pass

    def select_by_week(self, week):
        """根据周次查询"""
        pass

    def select_by_djz_and_xqj(self, djz, xqj, year, xq):
        """根据教师职工号第几周 星期几 学年学期 来查询"""
        return Js.objects.filter(Q(QSZ__lte=djz) | Q(JSZ__gte=djz), JSZGH=self.num, XQJ=xqj, KCZWMC__isnull=False,
                                 XN=year, XQ=xq).distinct().values('QSZ', 'JSZ', 'SJD', 'XQJ', 'SKCD', 'DSZ', 'JSMC', 'KCZWMC')

    def select_by_week_range(self, weeks, weeke):
        """根据周次weeks-weeke范围查找"""
        # 过滤需要加上年份，本次由于数据原因不可加上此条件
        result = Js.objects.filter(
            Q(QSZ__gte=weeks) | Q(JSZ__lte=weeke), JSZGH=self.num, KCZWMC__isnull=False,
        ).order_by('XQJ', 'SJD').values('QSZ', 'JSZ', 'SJD', 'XQJ', 'SKCD', 'DSZ', 'JSMC', 'KCZWMC')
        return result


class TtData:
    """
    调停课
    """
    def __init__(self, num=None):
        self.num = num

    def select_stop_by_num(self):
        """根据编号查询"""
        pass

    def select_stop_by_name(self):
        """根据姓名查询"""
        pass

    @staticmethod
    def select_by_kwargs(*args, **kwargs):
        return Tt.objects.filter(*args, **kwargs).values()


class RqData:
    @staticmethod
    def rq(weeks, weeke):
        """假日"""
        return Rq.objects.filter(Q(DJZ__gte=weeks) | Q(DJZ__lte=weeke), JJMC__isnull=False).values()

    @staticmethod
    def get_nyr(date):
        return Rq.objects.get(NYR=date)


class GlobalData:
    def __init__(self):
        pass

    @staticmethod
    def change_class(year):
        return GlobalKctj.objects.filter(XN__contains=year).values()


class FacClass:
    def __init__(self, num, weeks, weeke):
        self.date = DateFormat()
        self.num = num
        self.weeks = weeks
        self.weeke = weeke
        self.year_mon = self.date.current_time_to_academic_year()
        self.year = self.date.current_time_to_academic_xn()
        self.xq = self.date.current_time_to_academic_xq()
        self.js_obj = JsData(num=self.num)

    @property
    def js(self):
        return self.js_obj.select_by_week_range(self.weeks, self.weeke)

    def xs(self):
        pass

    @property
    def add_class(self):
        return TtData.select_by_kwargs(Q(XQSZ__gte=1) | Q(XJSZ__lte=self.weeke), XJSZGH=self.num,
                                       XKKH__contains=self.year_mon,)

    @property
    def stop_class(self):
        return TtData.select_by_kwargs(Q(XQSZ__gte=1) | Q(XJSZ__lte=20), XJSZGH=self.num,
                                       XKKH__contains=self.year_mon,)

    @property
    def jr_class(self):
        return RqData.rq(self.weeks, self.weeke)

    @property
    def global_class(self):
        global_class = GlobalData.change_class(self.year_mon)
        lis = defaultdict(list)
        for i in global_class:
            yr = RqData.get_nyr(i['YDATE'])
            xr = RqData.get_nyr(i['XDATE'])
            b = self.js_obj.select_by_djz_and_xqj(djz=yr.DJZ, xqj=yr.XQJ, year=self.year, xq=self.xq-1)# 这里因为数据问题 -1
            for i in b:
                i['XQJ'] = xr.XQJ
                lis[xr.DJZ].append(i)
        return lis
