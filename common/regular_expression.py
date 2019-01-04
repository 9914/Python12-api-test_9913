#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/22 20:06
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : regular_expression.py
# @Software : PyCharm
# @Explain  : 正则表达式替换

from common.basic_data import Context
import re

class Regular:
    def regular(self,case):
        # 正则匹配，获取request_data里面的mobilephone的值，结束是一个元组
        p = '\$\{(.*?)\}'
        while re.search(p,case):             #判断正则是否存在
            m = re.search(p,case)           #每次从case字符串里面获取一个正在进行替换
            key = m.group(1)                #获取到需要替换的字符串
            print("key",type(key),key)
            user = getattr(Context,key)     #去映射里面获取对应的值
            print("user",type(user),user)
            case = re.sub(p,user,case,count=1)#字符串替换
        return case
        # #findall = re.findall(pattern=p, string=case)
        # # 获取数据库最大mobilephone加1的值，结果是一个int型整数
        # mysql = MysqlUtill().get_fetch_one(sql=sql)
        # # 把数据库里面取到的最大mobilephone加1的值与request_data里面的mobilephone的值进行交换
        # #pattern: 正则中的模式字符串,repl: 替换的字符串，也可为一个函数,string: 要被查找替换的原始字符串
        # # 字符串替换：new_request_data = case.request_data.replace(findall[0], str(mysql))
        # new_request_data = re.sub(pattern=p, repl=str(mysql), string=case,count=1)
        # return new_request_data

# if __name__ == '__main__':
#     from common import http_path
#     import json
#     from common.Http_config import Reading
#     con = Reading(http_path.config_path_control)
#     config = con.get('CASE', 'button')
#     from common.http_reading_excel import DoExcel
#     excel_date = DoExcel(http_path.case_path, config)
#     # 注册
#     excel_date_register = excel_date.get_case('add')
#     for case in excel_date_register:
#         m = json.loads(Regular().regular(case=case["request_data"]))
#         print(m)