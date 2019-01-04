#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/25 20:37
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : basic_data.py
# @Software : PyCharm
# @Explain  : 反射类
from common.Http_config import Reading
from common import http_path
from common.mysql import MysqlUtill
class Context:
    #创建配置文件实例
    config = Reading(http_path.config_path_control)
    #获取数据库最大phone查询sql
    sql = config.get("SQL","sql_max_Phone")
    #获取配置文件里面项目用户
    normal_uesr = config.get('BASIC','normal_uesr')
    # 获取配置文件里面的购买用户
    Income_name = config.get('BASIC','Income_name')
    # 获取配置文件里面的pwd
    pwd =  config.get('BASIC','pwd')
    # 审核用户
    audit_user = config.get('BASIC', 'audit_user')
    # 查询项目用户MemberID
    Member = MysqlUtill().get_fetch_one(config.get("SQL", "sql_PayMemberId"))
    #用户不存在是，ID为空
    if Member is not None:
        PayMemberId = str(Member['Id'])
    else:
        print("反射类里面获取的：PayMemberId为None")
    # 查询购买用户MemberID
    Income = MysqlUtill().get_fetch_one(config.get("SQL", "sql_IncomeMemberId"))
    if Income is not None:
        IncomeMemberId = str(Income['Id'])
    else:
        print("反射类里面获取的：PayMemberId为None")
    #查询项目的全部id
    Loan = MysqlUtill().get_fetch_one(config.get("SQL", "sql_LoanId"))
    #还没有新增项目，ID为空
    if Loan is not None:
        LoanId = str(Loan['Id'])
    else:
        print("反射类里面获取的：LoanId为None")
    #最新的项目id
    an = MysqlUtill().get_fetch_one(config.get("SQL", "sql_anId"))
    if an is not None:
        anId = str(an['Id'])
    else:
        print("反射类里面获取的：anId为None")
    # 满标的项目ID
    mark = MysqlUtill().get_fetch_one(config.get("SQL", "Full_mark"))
    if mark is not None:
        Full_mark = str(mark['Id'])
    else:
        print("反射类里面获取的：Full_mark为None")
    #print(type(sql_anId),sql_anId)


