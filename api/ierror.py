# -*- coding: utf-8 -*-
"""
 @Time    : 2018/5/6 13:27
 @Author  : CyanZoy
 @File    : ierror.py
 @Description: 定义错误码含义
 """
# 41002	缺少 appid 参数
LACK_APPID = -40002
# 41003	缺少 sign 参数
LACK_SIGN = -40003
# 41004	缺少 userid 参数
LACK_USERID = -40004
# 41005	缺少 doorid 参数
LACK_DOORID = -40005
# 41006	缺少 timestamp 参数
LACK_TIMESTAMP = -40005

# 不合法的sign凭证
WRONGFUL_SIGN = -41000
# 不合法的timestamp
WRONGFUL_TIMESTAMP = -41001

# 错误的appid
WORNG_APPID = -42000

# timestamp时间戳过期
OVERDUE_TIME = -43000

# 验证不通过
VERIFICATION_NOT_PASS = -44000

# 账号非法(非教师账号，工号)
NUMBER_TYPE_ERROR = -45000
