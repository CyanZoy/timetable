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
        """根据当前的时间转换成毫秒后与夏令时或冬令时比较返回当前课程时间点"""
        # 夏令时
        summer = {'7:45-9:35': '1', '9:35-12:30': '3', '13:45-15:35': '6', '15:35-17:40': '8', '18:15-19:20': '10'}
        # 冬令时
        winner = {'7:45-9:35': '1', '9:35-12:30': '3', '13:15-15:05': '6', '15:05-17:10': '8', '17:45-18:50': '10'}
        h = self.t.tm_hour
        m = self.t.tm_min
        ds = []
        if self.t.tm_mon in range(5, 10):
            ds = summer
        else:
            ds = winner
        for a in ds:
            h_s, _, m_e = a.split(':')
            m_s, h_e = [int(w) for w in _.split('-')]
            if h*60*60*1000+m*60*1000 in range(int(h_s)*60*60*1000+m_s*60*1000, h_e*60*60*1000+int(m_e)*60*1000):
                return ds[a]


if __name__ == "__main__":
    print(DateFormat().current_time_to_academic_year())
