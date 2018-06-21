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

from scheduler.models import *
from django.db.models import Q


def test_one():
    a = set([c for c in GlobalKctj.objects.all()])
    for i, j in enumerate(a):
        print(i, j.EXCEPTTYPE_id)


def maxProfit():
    prices = [7,1,5,3,6,4]
    max = min = prices[0] if len(prices) else 0
    sum = 0
    for i in range(1, len(prices)):
        if prices[i] > min:
            max = prices[i] if prices[i] > max else max

        if prices[i] <= max:
            sum += max - min
            min = max = prices[i]
    return sum


def test_three():
    a = GlobalKctj.objects.filter(XN='2017-2018-2')
    print(a.values(), type(a))
    # print(a.XDATE, a.EXCEPTE, a.EXCEPTS, a.except_type_name)
    for h in a:
        b = Rq.objects.get(NYR=h.XDATE)
        print(b.XN, b.XQ, b.NYR, b.DJZ, b.XQJ)
        c = Xs.objects.filter(Q(QSZ__lte=b.DJZ) | Q(JSZ__gte=b.DJZ), XH='2015014257', XQJ=b.XQJ, XN=b.XN, XQ=b.XQ)\
            .values('XN', 'XQ', 'XH', 'QSZ', 'JSZ', 'XQJ', 'KCB')
        print(c, type(c))
        for i in c:
            print("---", type(i))
            name = i['KCB'].split('<br>')[0]
            d = LessonType.objects.filter(KCZWMC=name).values()
            for j in d:
                if j['KCLB'] == h.except_type_name:
                    # 课程类型相同，生成停课信息，是否显示停课标签将交由前端判断
                    stop = {'SJD': j['YSJD'], 'XQJ': j['YXQJ'], 'SKCD': 0, 'class_code': 'V007'}
                else:
                    print(False)


def test_four():
    import time, datetime
    # 夏令时
    summer = {'7:45-9:35': '1', '9:35-12:30': '3', '13:45-15:35': '6', '15:35-17:40': '8', '18:15-19:20': '10'}
    # 冬令时
    winner = {'7:45-9:35': '1', '9:35-12:30': '3', '13:15-15:05': '6', '15:05-17:10': '8', '17:45-18:50': '10'}
    b = time.localtime(time.time())
    h = b.tm_hour
    m = b.tm_min
    if 11 in range(5, 10):
        ds = summer
    else:
        ds = winner
    for a in ds:
        """根据当前时间转换成毫秒，与夏令时与冬令时比较，返回上课节次"""
        h_s, _, m_e = a.split(':')
        m_s, h_e = [int(w) for w in _.split('-')]
        if h*60*60*1000+m*60*1000 in range(int(h_s)*60*60*1000+m_s*60*1000, h_e*60*60*1000+int(m_e)*60*1000):
            return ds[a]


def test_five():
    x = 43
    y =False
    print(x>=y and 'A'<'B' and not y)


def test_six():
    list1 = [4, 5, 6]
    list2 = list1
    list1[2] = 3
    print(list2)


if __name__ == '__main__':
    # j = test_four()
    # print('第%s节' % j)
    test_six()