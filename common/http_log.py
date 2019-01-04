#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/15 13:40
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : http_log.py
# @Software : PyCharm
# @Explain  : 日志文件

from common import http_path
from common.Http_config import Reading
import logging
import time
import os
import HTMLTestRunnerNew
from logging.handlers import TimedRotatingFileHandler   #根据时间进行滚动
from logging.handlers import RotatingFileHandler    #根据文件大小进行滚动
# 创建日志，并设置级别
my_log = logging.getLogger(Reading(http_path.config_path_control).get('LOG','logger_name'))
my_log.setLevel(Reading(http_path.config_path_control).get('LOG','log_level'))

def set_handler(level):     # 对接渠道和文件
    if level == 'ERROR':    #判断级别是否是ERROR，是，就对接error_handler
        my_log.addHandler(HttpLog.error_handler)
    else:
        my_log.addHandler(HttpLog.file_handler)     #否，对接file_handler
    my_log.addHandler(HttpLog.handler)              # 那个级别的日志，在控制台console中显示
    #my_log.addHandler(HttpLog.report_handler)       # 全部输出到report

def remove_handler(level):     #移除链接
    if level == 'ERROR':
        my_log.removeHandler(HttpLog.error_handler)
    else:
        my_log.removeHandler(HttpLog.file_handler)
    my_log.removeHandler(HttpLog.handler)
    #my_log.addHandler(HttpLog.report_handler)       # 全部输出到report

def get_log_dir():  # 获取当天的日志存放目录
    log = os.path.join(http_path.log_path,get_current_day())  #基本路径+当天时间
    if not os.path.isdir(log):  #判断是否有当天时间的日志目录
        os.makedirs(log)        #没有新建一个目录
    return log

def get_current_day():  # 获取当天时间
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

class HttpLog:
    info_file = os.path.join(get_log_dir(), 'info.log')     #最终日志路径
    error_file = os.path.join(get_log_dir(), 'error.log')
    #日志输出格式
    farmatter = logging.Formatter(Reading(http_path.config_path_control).get('LOG','formatter'))
    #创建渠道，设置级别，输出格式, 控制台输出
    handler = logging.StreamHandler()
    handler.setLevel(Reading(http_path.config_path_control).get('LOG','handler_level'))
    handler.setFormatter(farmatter)
    # 创建本地INFO级别的日志文件，输出格式
    # 写入文件，如果文件超过5M，仅保留5个文件。
    file_handler = logging.handlers.RotatingFileHandler(
        filename=info_file, maxBytes=1024*1024*5, backupCount=5, encoding='utf-8', delay=False)
    file_handler.suffix = "%Y-%m-%d_%H-%M.log"
    file_handler.setLevel(Reading(http_path.config_path_control).get('LOG','info_level'))
    file_handler.setFormatter(farmatter)
    # 创建本地ERROR级别的日志文件，输出格式
    # 添加TimedRotatingFileHandler
    # 定义一个1天换一次log文件的handler
    # 保留3个旧log文件
    error_handler = logging.handlers.TimedRotatingFileHandler(
        filename=error_file,when='D', interval=1, backupCount=3, encoding='utf-8')
    error_handler.suffix = "%Y-%m-%d_%H-%M.log"
    error_handler.setLevel(Reading(http_path.config_path_control).get('LOG', 'error_level'))
    error_handler.setFormatter(farmatter)
    # 报表日志输出,在控制台展示
    report_handler = logging.StreamHandler(HTMLTestRunnerNew.stdout_redirector)
    report_handler.setLevel(Reading(http_path.config_path_control).get('LOG', 'report_level'))
    report_handler.setFormatter(farmatter)

#创建日志级别函数
    @staticmethod
    def debug(msg):
        set_handler('DEBUG')
        my_log.debug(msg)
        remove_handler('DEBUG')

    @staticmethod
    def info(msg):
        set_handler('INFO')
        my_log.info(msg)
        remove_handler('INFO')

    @staticmethod
    def error(msg):
        set_handler('ERROR')
        my_log.error(msg, exc_info=True)  # 同时输出异常信息
        remove_handler('ERROR')

if __name__ == '__main__':
    try:
        raise AssertionError
    except AssertionError as e:
        HttpLog.info('info!!!!')
        HttpLog.error('error!!!!')
        HttpLog.debug('debug!!!!')





