#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/15 15:49
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : A_02_Login_test_case.py
# @Software : PyCharm
# @Explain  : 登录测试用例

from ddt import ddt,data,unpack
from common.http_requests_01 import HttpRequest
from common.http_reading_excel_01 import DoExcel
from common import http_path
from common.Http_config import Reading
from common.http_log import HttpLog
from common.regular_expression import Regular
import unittest
import json
#创建日志对象，装载日志
my_log = HttpLog()
#创建取配置对象
con = Reading(http_path.config_path_control)
#获取需要的执行的测试用例ID
config = con.get('CASE','button')
#读取配置文件里面的URL地址
config_url = con.get('URL','url_date')
#读取测试数据,实例化测试数据对象
excel_date = DoExcel(http_path.case_path,config)
#登录
excel_date_login = excel_date.get_case('login')

@ddt
class HttpCase(unittest.TestCase):
    # 加 * 号，去掉一层外套
    @data(*excel_date_login)
    #@unpack
    def test_http_case(self,i):
        date = Regular().regular(i.request_data)  # 正则参数替换
        my_log.info('正在执行地{0}条用例; 用例名称:{1}; 用例说明:{2}; 用例接口:{3}'.
                    format(i.case_id, i.case_name, i.case_rept, i.api_name))
        my_log.info('================检查url====================')
        my_log.info('url:{}'.format(config_url+i.url))
        my_log.info('================检查request_data====================')
        my_log.info('request_data:{}'.format(i.request_data))
        my_log.info('================检查替换后的date====================')
        my_log.info('request_data:{}'.format(date))
        my_log.info('================检查method====================')
        my_log.info('method:{}'.format(i.mathod))
        my_log.info('================检查api_name====================')
        my_log.info('api_name:{}'.format(i.api_name))
        my_log.info('================检查预期结果expected_data====================')
        my_log.info('expected_data:{}'.format(i.expected_data))
        res = HttpRequest(config_url+i.url,json.loads(date),i.mathod)
        my_log.info('实际结果:{}'.format(res.get_json()))
        my_log.info('=================开始断言==================')
        try:
            #断言判断实际结果与期望结果是否一致
            self.assertEqual(json.loads(i.expected_data)['code'],json.loads(res.get_text())['code'])
            Testresult = 'pass'
        except Exception as e:
            Testresult = 'failed'
            my_log.error('断言错误:{0}'.format(e))
            raise e
        finally:
            my_log.info('resultd的值是:{0}'.format(Testresult))
            my_log.info('=================结束断言==================')
            #写入实际结果actual和result值
            excel_date.write_by_case_id(sheet_name='login', case_id=i.case_id,
                                        actual=res.get_text(), result=Testresult)

# if __name__ == '__main__':
#     unittest.main()
