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
# a = Js.objects.values('JSZGH').distinct().order_by('JSZGH')
# a = Js.objects.filter(KCZWMC__contains="工程")
# for _ in a:
#     print(_.JSZGH, _.QSZ, _.JSZ, _.KCZWMC)

