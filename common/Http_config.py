#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/15 13:27
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : Http_config.py
# @Software : PyCharm
# @Explain  : 配置文件读取类
import configparser
from common import http_path
class Reading:
    def __init__(self,name):
        self.name = name
        try:
            self.con = configparser.ConfigParser()  # 创建一个config对象
            self.con.read(self.name, encoding='utf-8')  # 读取那个配置文件
            if self.con.getboolean('CONTROL', 'on'):
                self.con.read(http_path.config_path, encoding='utf-8')
            else:
                self.con.read(http_path.config_path_mysql, encoding='utf-8')
        except FileNotFoundError as e:
            print("配置文件名错误：{0}".format(e))
            raise e
    def get(self,sections,options):
        #  #返回str类型的值  读取哪一行的那条数据
        try:
            return self.con.get(sections,options)
        except Exception as e:
            print('sections or options error：{0}'.format(e))
            raise e
    def get_boolean(self,sections,options):
        #  #返回boolean类型的值  读取哪一行的那条数据
        try:
            return self.con.getboolean(sections,options)
        except Exception as e:
            print('sections or options error：{0}'.format(e))
            raise e
    def get_int(self,sections,options):
        #  #返回int类型的值  读取哪一行的那条数据
        try:
            return self.con.getint(sections,options)
        except Exception as e:
            print('sections or options error：{0}'.format(e))
            raise e
    def get_float(self,sections,options):
        #  #返回float类型的值  读取哪一行的那条数据
        try:
            return self.con.getfloat(sections,options)
        except Exception as e:
            print('sections or options error：{0}'.format(e))
            raise e

# if __name__ == '__main__':
#     from common import http_path
#     m = Reading(http_path.config_path_control).get('LOG','handler_level')
#     print(type(m),m)