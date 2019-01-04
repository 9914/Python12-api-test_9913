#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/15 14:19
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : http_path.py
# @Software : PyCharm
# @Explain  : 常量路径文件

import os
#原始路径
#data_path_01 = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
data_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#配置文件路径  join 路径拼接
config_path = os.path.join(data_path,'config','http_config')
config_path_control = os.path.join(data_path,'config','control')
config_path_mysql = os.path.join(data_path,'config','mysql')
#测试数据路径
case_path= os.path.join(data_path,'test_case','testdatas.xlsx')
#测试报告路径
reprot_path = os.path.join(data_path,'test_result','html_report','前程贷API接口测试报告.html')
#日志路径
log_path = os.path.join(data_path,'test_result','logs')
#test_case路径
test_path = os.path.join(data_path,'Interface_API')
#print(data_path)