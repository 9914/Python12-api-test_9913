"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2019/1/3 11:23
# @Author    : Python12_9913_秋     
# @Email     : 793630871@qq.com    
# @File      : http_logs             
# @Software  : PyCharm    
# @User      ：skw             
# @Project   ：Python12-api-test_9913      
# @Explain   : 日志文件类
"""
from common import http_path
from common.Http_config import Reading
import logging
import time
import os
import HTMLTestRunnerNew
from logging.handlers import TimedRotatingFileHandler   #根据时间进行滚动
from logging.handlers import RotatingFileHandler    #根据文件大小进行滚动

my_log = logging.getLogger(Reading(http_path.config_path_control).get('LOG','logger_name'))
my_log.setLevel(Reading(http_path.config_path_control).get('LOG','log_level'))
leve = Reading(http_path.config_path_control)
fmt = " %(asctime)s  %(levelname)s %(filename)s %(funcName)s [ line:%(lineno)d ] %(message)s"
        #%%(asctime)s-%%(levelname)s-%%(filename)s-%%(funcName)-s[line:%%(lineno)d]-%%(name)s
fmt1 = leve.get('LOG','formatter')
datefmt = '%a, %d %b %Y %H:%M:%S'
Console = logging.StreamHandler()
#格式Fri, 03 Aug 2018 17:02:05 周几+日期+月份+年份+时+分+秒
curTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))

def get_log_dir():  # 获取当天的日志存放目录
    log = os.path.join(http_path.log_path,curTime)  #基本路径+当天时间
    if not os.path.isdir(log):  #判断是否有当天时间的日志目录
        os.makedirs(log)        #没有新建一个目录
    return log

info_file = os.path.join(get_log_dir(), 'info.log')     #最终日志路径
error_file = os.path.join(get_log_dir(), 'error.log')

cons = logging.basicConfig(format=fmt1,datefmt=datefmt,level=leve.get('LOG','handler_level'),handlers=[Console])
my_log.info('ssssss')