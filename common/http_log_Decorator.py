"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2019/1/2 11:36
# @Author    : Python12_9913_秋     
# @Email     : 793630871@qq.com    
# @File      : http_log_Decorator             
# @Software  : PyCharm    
# @User      ：skw             
# @Project   ：Python12-api-test_9913      
# @Explain   : 日志装饰器
"""
from common.Http_config import Reading
from common.http_log import HttpLog
from common import http_path
from common.http_reading_excel_01 import DoExcel
my_log = HttpLog()
con = Reading(http_path.config_path_control)
config_url = con.get('URL', 'url_date')
def Decorator(name):
    def log(func):
        def sub_log(*args,**kwargs):
            print('正在执行地{0}条用例; 用例名称:{1}; 用例说明:{2}; 用例接口:{3}'.
                        format(i.case_id, i.case_name, i.case_rept, i.api_name))
            my_log.info('================检查url====================')
            my_log.info('url:{}'.format(config_url + i.url))
            my_log.info('================检查request_data====================')
            my_log.info('request_data:{}'.format(i.request_data))
            my_log.info('================检查替换后的request_data====================')
            my_log.info('request_data:{}'.format(date))
            my_log.info('================检查method====================')
            my_log.info('method:{}'.format(i.mathod))
            my_log.info('================检查api_name====================')
            my_log.info('api_name:{}'.format(i.api_name))
            my_log.info('================检查预期结果expected_data====================')
            my_log.info('expected_data:{}'.format(i.expected_data))
            func(*args, **kwargs)
        return sub_log
    return log

if __name__ == '__main__':
    con = Reading(http_path.config_path_control)
    # 获取需要的执行的测试用例ID
    config = con.get('CASE', 'button')
    excel_date = DoExcel(http_path.case_path, config)
    # 注册
    excel_date_register = excel_date.get_case('register')
    print(Decorator(excel_date_register))
