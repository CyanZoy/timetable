# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/18 9:45
 @Author  : CyanZoy
 @File    : date_format.py
 @Software: PyCharm
 """
import time
from utils import constants


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


class DateFormat:
    """操纵时间"""
    def __init__(self):
        self.time = time.time()

    # @property
    def current_time_n_y_r(self, default_sign='-'):
        """获取n-y-r"""
        return time.strftime('%Y'+default_sign+'%m'+default_sign+'%d', time.localtime(self.time))

    def current_time_to_academic_year(self):
        """获取当前学年
        @:return Y-Y-N -> 2017-2018-1 -> 学年加学期
        """
        t = time.localtime(self.time)
        year = t.tm_year
        month = t.tm_mon
        if month in constants.SEMESTER_ONE:
            n = 1
        else:
            n = 2
        if month in range(9, 13):
            """9-12个月 学年为当前学年 至 学年+1"""
            return '%s-%s-%s' % (year, year+1, n)
        else:
            return '%s-%s-%s' % (year-1, year, n)


if __name__ == "__main__":
    print(DateFormat().current_time_to_academic_year())
