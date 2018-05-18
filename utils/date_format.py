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
        self.t = time.localtime(self.time)
        self.year = self.t.tm_year
        self.month = self.t.tm_mon

    # @property
    def current_time_n_y_r(self, default_sign='-'):
        """获取n-y-r"""
        return time.strftime('%Y'+default_sign+'%m'+default_sign+'%d', time.localtime(self.time))

    def current_time_to_academic_year(self):
        """获取当前学年
        @:return Y-Y-N -> 2017-2018-1 -> 学年加学期
        """

        if self.month in constants.SEMESTER_ONE:
            n = 1
        else:
            n = 2
        if self.month in range(9, 13):
            """9-12个月 学年为当前学年 至 学年+1"""
            return '%s-%s-%s' % (self.year, self.year+1, n)
        else:
            return '%s-%s-%s' % (self.year-1, self.year, n)

    def current_time_to_academic_xn(self):
        """根据当前时间返回当前学年"""
        if self.month in range(9, 13):
            """9-12个月 学年为当前学年 至 学年+1"""
            return '%s-%s' % (self.year, self.year + 1)
        else:
            return '%s-%s' % (self.year - 1, self.year)

    def current_time_to_academic_xq(self):
        """根据当前时间返回当前学期"""
        if self.month in constants.SEMESTER_ONE:
            return 1
        return 2

    def current_time_to_sjd(self):
        """根据当前的时间返回当前时间点，第几周，学年"""


if __name__ == "__main__":
    print(DateFormat().current_time_to_academic_year())
