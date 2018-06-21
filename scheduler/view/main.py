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
    def __init__(self, num, name=None, year=None):
        self.num = num
        self.name = name
        self.year = year
        if not self.year:
            self.year = DateFormat().current_time_to_academic_year()

    def select_by_name(self, name):
        """根据姓名查找"""
        pass

    def select_by_number(self):
        """根据教师职工号查找"""
        pass

    def select_student_xkkh_by_number(self, xn, xq):
        """根据学生学号查询课程 过滤条件 学年学期"""
        return Xs.objects.filter(XH=self.num, XN=xn, XQ=xq)

    def select_by_week(self, week):
        """根据周次查询"""
        pass

    def select_by_djz_and_xqj(self, djz, xqj, year, xq):
        """根据教师职工号第几周 星期几 学年学期 来查询"""
        return Js.objects.filter(Q(QSZ__lte=djz) | Q(JSZ__gte=djz), JSZGH=self.num, XQJ=xqj, KCZWMC__isnull=False,
                                 XN=year, XQ=xq).distinct().values('QSZ', 'JSZ', 'SJD', 'XQJ', 'SKCD', 'DSZ', 'JSMC', 'KCZWMC')

    def select_student_by_djz_and_xqj(self, djz, xqj, year, xq):
        """根据学生卡号, 第几周 星期几 学年学期 来查询"""
        return Xs.objects.filter(Q(QSZ__lte=djz) | Q(JSZ__gte=djz), XH=self.num, XQJ=xqj, XN=year, XQ=xq
                                 ).distinct().values('XN', 'XQ', 'XH', 'QSZ', 'JSZ', 'DJJ', 'XQJ', 'SKCD', 'DSZ', 'KCB')

    def select_student_by_djz_and_xqj_queryset(self, djz, xqj, year, xq):
        """根据学生卡号, 第几周 星期几 学年学期 来查询"""
        return Xs.objects.filter(Q(QSZ__lte=djz) | Q(JSZ__gte=djz), XH=self.num, XQJ=xqj, XN=year, XQ=xq
                                 ).distinct()

    def select_by_week_range(self, weeks, weeke, **kwargs):
        """根据周次weeks-weeke范围查找"""
        # 过滤需要加上年份，本次由于数据原因此条件为2017-2018-1
        result = Js.objects.filter(
            Q(QSZ__gte=weeks) | Q(JSZ__lte=weeke), JSZGH=self.num, KCZWMC__isnull=False, XKKH__contains='2017-2018-1', **kwargs
        ).order_by('XQJ', 'SJD').values('QSZ', 'JSZ', 'SJD', 'XQJ', 'SKCD', 'DSZ', 'JSMC', 'KCZWMC')
        return result

    def select_by_one_week(self, week, **kwargs):
        """根据周次查找"""
        # 过滤需要加上年份，本次由于数据原因此条件为2017-2018-1
        result = Js.objects.filter(
            Q(QSZ__lte=week) & Q(JSZ__gte=week), JSZGH=self.num, KCZWMC__isnull=False, XKKH__contains='2017-2018-1', **kwargs
        ).order_by('XQJ', 'SJD').values('QSZ', 'JSZ', 'SJD', 'XQJ', 'SKCD', 'DSZ', 'JSMC', 'KCZWMC')
        return result

    def select_student_by_week_range(self, weeks, weeke, xn, xq):
        """根据学生学号，周次范围，学年学期"""
        result = Xs.objects.filter(
            Q(QSZ__gte=weeks) | Q(JSZ__lte=weeke), XH=self.num, XN=xn, XQ=xq,
        ).order_by('XQJ', 'DJJ').values('QSZ', 'JSZ', 'DJJ', 'XQJ', 'SKCD', 'DSZ', 'KCB')
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
        print('date=111', date)
        return Rq.objects.get(NYR=date)


class GlobalData:
    def __init__(self):
        pass

    @staticmethod
    def change_class(year):
        return GlobalKctj.objects.filter(XN__contains=year).values()

    @staticmethod
    def get_global_by_xn(xn):
        return GlobalKctj.objects.filter(XN=xn)


class FacClass:
    def __init__(self, num, weeks, weeke, t):
        self.date = DateFormat()
        self.num = num
        self.weeks = weeks
        self.weeke = weeke
        self.year_mon = self.date.current_time_to_academic_year()
        self.year = self.date.current_time_to_academic_xn()
        self.xq = self.date.current_time_to_academic_xq()
        self.js_obj = JsData(num=self.num)
        self.t = t

    @property
    def js(self):
        return self.js_obj.select_by_week_range(self.weeks, self.weeke)

    def js_kwargs(self, **kwargs):
        return self.js_obj.select_by_week_range(self.weeks, self.weeke, **kwargs)

    def js_by_one_week(self, **kwargs):
        return self.js_obj.select_by_one_week(self.weeks, **kwargs)

    @property
    def xs(self):
        return self.js_obj.select_student_by_week_range(weeks=self.weeks, weeke=self.weeke, xn=self.year, xq=self.xq)

    @property
    def add_class(self):
        return TtData.select_by_kwargs(Q(XQSZ__gte=1) | Q(XJSZ__lte=self.weeke), XJSZGH=self.num,
                                       XKKH__contains=self.year_mon,)

    @property
    def stop_class(self):
        return TtData.select_by_kwargs(Q(XQSZ__gte=1) | Q(XJSZ__lte=20), YJSZGH=self.num,
                                       XKKH__contains=self.year_mon,)

    @property
    def xs_extract_class(self):
        xk = self.js_obj.select_student_xkkh_by_number(xn=self.year, xq=self.xq).values()
        extract = []
        for _ in xk:
            tt = TtData.select_by_kwargs(XKKH=_['XKKH'])
            if tt:
                for w in tt:
                    extract.append(w)
        return extract

    def xs_add_class(self):
        pass

    @property
    def jr_class_week(self):
        """假日"""
        return RqData.rq(self.weeks, self.weeke)

    @property
    def jr_class_nyr(self):
        """假日"""
        return RqData.get_nyr(self.date.current_time_n_y_r())

    @property
    def global_class(self):
        """生成全局调课中调课的信息"""
        global_class = GlobalData.change_class(self.year_mon)
        lis = defaultdict(list)
        for i in global_class:
            yr = RqData.get_nyr(i['YDATE'])
            xr = RqData.get_nyr(i['XDATE'])
            if self.t == '1':
                b = self.js_obj.select_by_djz_and_xqj(djz=yr.DJZ, xqj=yr.XQJ, year=self.year, xq=self.xq-1)# 这里因为数据问题-1
            else:
                b = self.js_obj.select_student_by_djz_and_xqj(djz=yr.DJZ, xqj=yr.XQJ, year=self.year, xq=self.xq)
            for j in b:
                # print('b=', b)
                j['XQJ'] = xr.XQJ
                lis[xr.DJZ].append(j)
        return lis

    @property
    def global_class_stop(self):
        """生成全局调课中需要停课的数据"""
        from collections import defaultdict
        a = GlobalData.get_global_by_xn(self.year_mon)
        lis = defaultdict(list)
        for h in a:
            b = RqData.get_nyr(h.XDATE)
            c = self.js_obj.select_student_by_djz_and_xqj_queryset(b.DJZ, b.XQJ, b.XN, b.XQ)
            for i in c:
                name = i.KCB.split('<br>')[0]
                d = LessonType.objects.filter(KCZWMC=name).values()
                for j in d:
                    if j['KCLB'] == h.except_type_name:
                        # 课程类型相同，生成停课信息，是否显示停课标签将交由前端判断
                        stop = {'SJD': h.EXCEPTS, 'XQJ': i.XQJ, 'SKCD': 0, 'class_code': 'V007'}
                        lis[b.DJZ].append(stop)
            return lis

