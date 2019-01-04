#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/22 17:57
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : mysql.py
# @Software : PyCharm
# @Explain  : MYsql数据量链接
"""
1.链接数据库
2.编写sql
3.建立游标
4.执行
"""
from common import http_path
from common.Http_config import Reading
import pymysql
class MysqlUtill:
    def __init__(self):
        #获取配置文件里面的MySQL配置
        config = Reading(http_path.config_path_control)
        host = config.get('MYSQL', 'Host_name')
        port = config.get_int('MYSQL', 'port')          #port是一个数字，使用getint
        user = config.get('MYSQL', 'user')
        pwd = config.get('MYSQL', 'pwd')
        try:
            self.mysql = pymysql.connect(host=host, user=user, password=pwd,
             database='future',port=port,cursorclass=pymysql.cursors.DictCursor)
            #cursorclass=pymysql.cursors.DictCursor  返回字典格式
        except BaseException as e:
            print("数据库链接异常：{}".format(e))
            raise e
    def get_fetch_one(self,sql):
        #查询一条数据并返回数据
        cursor = self.mysql.cursor()        #建立游标
        cursor.execute(sql)                  #根据sql进行查询
        date = cursor.fetchone()           #返回一条数据
        #max_phone = eval(phone["MobilePhone"]) + 1      #字符串格式
        return date

    def get_fetch_all(self,sql):
        cursor = self.mysql.cursor()        # 建立游标
        cursor.execute(sql)                 # 根据sql进行查询
        date = cursor.fetchall()          # 返回多条数据,如获取用户列表，标列表等
        #max_phone = (phone[0]) + 1           # 返回的是元组嵌套格式
        return date

    def get_fetch_many(self,sql):
        cursor = self.mysql.cursor()        # 建立游标
        cursor.execute(sql)                 # 根据sql进行查询
        date = cursor.fetchmany()           # 指定返回多少条数据
        #max_phone = eval(phone[0]) + 1
        return date


if __name__ == '__main__':
    sql = 'SELECT Id FROM financelog WHERE IncomeMemberId =(SELECT Id FROM member WHERE MobilePhone = 18999999653) ORDER BY Id DESC'
    print(sql)
    m = MysqlUtill().get_fetch_one(sql=sql)         #结果是元组
    print(type(m),m)
