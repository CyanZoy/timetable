# -*- coding: utf-8 -*-
"""
 @Time    : 2018/6/3 16:12
 @Author  : CyanZoy
 @File    : open.py
 @Describe:     判断能否开门
 """
from scheduler.view.main import *
from utils.date_format import *

tim = DateFormat()
we = RqData.get_nyr(tim.current_time_n_y_r())
sjd = tim.current_time_to_sjd()
# we 日期对象， sjd为当前时间对应的课程节次


def class_constant(lesson, doorid):
    """固定课程"""
    if lesson:
        for i in lesson:
            if we.DJZ in range(i['QSZ'], i['JSZ']+1) and doorid in i['JSMC']:
                return True
    return False


def class_makeup(lesson):
    """补课"""

    pass


def class_stop(lesson):
    """停课"""
    if lesson:
        for i in lesson:
            print('class_stop=', i)
            if i['BDLB'] in ['调课', '停课', '换教师', '换地点'] and i['YSJD'] == sjd and i['YXQJ'] == we.XQJ and we.DJZ in range(i['YQSZ'], i['YJSZ']):
                return True
    else:
        return False
    pass


def class_global(lesson):
    """全校性调课"""
    pass


def can_open(num, t=1, doorid=None):
    """
    判断能否开门
    :param num: 账号
    :param t:1 为教师
    :param doorid: 门号
    :return: 开门判断和原因
    """
    flag = False
    msg = '无'
    if sjd is None:
        # 判断是否上课时间
        flag = False
        msg = '非上课时间'
        # return flag, msg
    fac = FacClass(num, we.DJZ, we.DJZ, t)
    # 查询是否节假日
    jr = fac.jr_class_nyr
    if jr.JJMC:
        flag = False
        msg = jr.JJMC
        return flag, msg
    # 查询固定课程
    js = fac.js_by_one_week(SJD=3, XQJ=we.XQJ)
    if class_constant(js, doorid):
        # 是否停课
        tk = fac.stop_class
        if class_stop(tk):
            pass
        # 存在停课 判断是否存在补课
            # 存在补课 flag = True

            # 不存在补课 判断是否存在全校性调课

                #存在全校性调课 flag = Y

                #不存在全校性调课 则 flag = N

        else:
            flag = True
        # 不存在停课 则 flag = True

        pass

    else:
        # 不存在固定课程 -> 判断是否存在补课
            # 存在补课flag = Y

            # 不存在补课
                # 存在全校性调课

                # 不存在全校性调课
        pass


    # for i in tk:
    #     # print(i)
    #     if i['BDLB'] in ['调课', '停课', '换教师', '换地点']:
    #         if i['YSJD'] == sjd:
    #             msg = i['BDLB'] + '原'
    #             flag = False


    return flag, msg


