# from django.test import TestCase
import cx_Oracle, os

# os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  ##保证编码一致
# os.environ['path'] =  'C:\Program Files (x86)\Oracle\instantclient_12_2'
# db = cx_Oracle.connect('TIMETABLE', 'timetable', '10.60.144.34/TIMETABLE')
# conn = cx_Oracle.connect('TIMETABLE/timetable@10.60.144.34:1521/orcl')
# print("oracle版本：", conn.version)
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "timetable.settings")
django.setup()
from django.contrib.auth import REDIRECT_FIELD_NAME
#
#
# funcs = [lambda y, x, n=n: y+n for n in range(5)]
# for f in funcs:
#     print(f(1, 2))
# from django.db import connection
from scheduler.models import *
from scheduler.view.main import ChangeList
import json
# a = Js.objects.values('JSZGH').distinct().order_by('JSZGH')
from utils.date_format import *

# def tete(*args):
#     a = Js.objects.filter(JSZGH='1999900109', KCZWMC__isnull=False, QSZ__lte=1, JSZ__gte=1).order_by(*args)[:1000].values()
#     import json
#     lis = {"1": []}
#     for _ in a:
#         # lis["1"].append(_)
#         print(_)
#
#
# def date_handler(obj):
#     return obj.isoformat() if hasattr(obj, 'isoformat') else obj
#
# tete('XQJ')


# chan = ChangeList(Js, 1000, JSZGH='1999900109', KCZWMC__isnull=False)#, QSZ__lte=1, JSZ__gte=1
# result = chan.get_result_by_range('XQJ', 'SJD')
# from collections import defaultdict
# lis = defaultdict(list)
# lis['week'] = 1
# rmp = {
#     ord('单'): '1',
#     ord('双'): '2',
# }
# for i in result:
#     i['DSZ'] = i['DSZ'].replace('单', '1').replace('双', '2')
#     lis['1'].append(i)
# lis = json.dumps(lis, default=date_handler, ensure_ascii=False)
# print(lis)

from django.db.models import Q
from scheduler.view.main import *

# def tee(*args, **kwargs):
#     a = Js.objects.filter(*args, **kwargs)
#     for _ in a:
#         print(_.KCZWMC, _.JSZGH)
#
#
# tee((Q(KCZWMC__contains="工程") | Q(JSZGH__contains="2002900058")), KCZWMC__isnull=False)
#

# pag = Pagina(Js, 1, 25, (Q(KCZWMC__contains="工程") | Q(JSZGH__contains="2002900058")), KCZWMC__isnull=False)
#
# result = pag.result
# for _ in result:
#     print(_.KCZWMC, _.JSZGH)

from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required

# @permission_required('auth.can_add_user', login_url='/login/')
# def tee():
#     user = User.objects.get(username='test')
#     a = user.user_permissions.all()
#     print(a)
#     for _ in a:
#         print(_)
#
# tee()
from utils.date_format import DateFormat
# current_time = DateFormat.current_time_n_y_r()
# rq = Rq.objects.latest('DJZ')
# a = Rq.objects.last()
# print(a)
# print(rq)
# print(rq.NYR, rq['DJZ'])
# a = Rq.objects.filter(DJZ=5)
# print(a.latest('-NYR').NYR, a.latest('NYR').NYR)
import numpy as np
sign = np.zeros(shape=(12, 8), dtype=bool)
"""课表总test"""
w = 8
#  初始化ChangeList对象
chan = ChangeList(Js, 1000, JSZGH=str(2000900075), KCZWMC__isnull=False, QSZ__lte=w, JSZ__gte=w)
#  查询出JSZGH的第w周课程, 以星期几和时间点来排序
# result = chan.get_result_by_range('XQJ', 'SJD').values('SJD', 'JSZGH', 'QSZ', 'JSZ', 'XQJ', 'SJD', 'SKCD', 'DSZ', 'JSMC', 'KCZWMC')
from django.db.models import Q
# for _ in result:
#     # print(_)
#     sign[int(_['SJD']), int(_['XQJ'])] = True

# 以下查询新添课程包括补课，调课，换教师，停课，过滤条件为学年，教师工号或姓名，周次
extract = Tt.objects.filter(Q(XJSZGH=str(2001900030)) | Q(XJSZGH='丛海彬') | Q(YJSZGH=str(2003900010)),
                            XQSZ__lte=5, XJSZ__gte=5,
                            XKKH__contains='2007-2008-1'
                            ).values()
# # 停课
# extract2 = Tt.objects.filter(Q(XJSZGH=str(2003900010)) | Q(XJSZGH='丛海彬'),
#                             XQSZ__lte=5, XJSZ__gte=5,
#                             XKKH__contains='2007-2008-1'
#                             ).values()


# if extract:
#     for _ in extract:
#         if _['BDLB'] in ['调课', '补课', '换教师']:
#             print(_['BDLB'], _['BDBH'], _['XKKH'], _['YJSZGH'], _['YQSZ'], _['YJSZ'], _['YXQJ'], _['YSJD'], _['YSKCD'], '新', _['XJSZGH'], _['XQSZ'], _['XJSZ'], _['XXQJ'], _['XSJD'], _['XSKCD'])
#         elif _['BDLB'] in ['停课']:
#             print(_['BDLB'], _['BDBH'], _['XKKH'], _['YJSZGH'], _['YQSZ'], _['YJSZ'], _['YXQJ'], _['YSJD'], _['YSKCD'], '新', _['XJSZGH'], _['XQSZ'], _['XJSZ'], _['XXQJ'], _['XSJD'], _['XSKCD'])
#             print({'SJD': _['YSJD'], 'XQJ': _['YXQJ'], 'SKCD': _['YSKCD'], 'DSZ': '', 'class_code': 'V002'})


# year_mon = DateFormat().current_time_to_academic_year()
# extract_s = Tt.objects.filter((Q(YJSZGH=str(2003900091)) | Q(YJSZGH='丛海彬')),
#                               YQSZ__lte=w, YJSZ__gte=w,
#                               XKKH__contains=year_mon,
#                               ).values()
# for i in extract_s:
#     print(i)

from collections import defaultdict
week = [1, 2, 3, 4, 5, 6, 7, 8, 9]
num = '1999900171'
lis = defaultdict(list)
start_time = time.time()
# for w in week:
result = Js.objects.filter(Q(QSZ__lte=min(week)) | Q(JSZ__gte=max(week)),
    JSZGH=str(num), KCZWMC__isnull=False,
).order_by('XQJ', 'SJD').values('QSZ', 'JSZ', 'SJD', 'XQJ', 'SKCD', 'DSZ', 'JSMC', 'KCZWMC')

for i in result:
    for w in week:
        if w in range(i['QSZ'], i['JSZ']+1):
            lis[w].append(i)


b = json.dumps(lis, ensure_ascii=False)
print(b)

print(time.time() - start_time)


liss = [1, 2, 3, 4]
print(liss[1::2])
