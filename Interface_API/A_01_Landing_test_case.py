#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/15 15:49
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : A_01_Landing_test_case.py
# @Software : PyCharm
# @Explain  : 注册测试用例

from ddt import ddt,data,unpack
from common.http_requests_01 import HttpRequest
from common.http_reading_excel_01 import DoExcel
from common import http_path
from common.Http_config import Reading
from common.http_log import HttpLog
from common.mysql import MysqlUtill
from common.basic_data import Context
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
#注册
excel_date_register = excel_date.get_case('register')

@ddt
class HttpCase(unittest.TestCase):
    def setUp(self):
        global sql_max_Phone,tel_phone,max_phone
        #获取配置文件里面的最大值电话号码查询sql
        sql_max_Phone = con.get('SQL', 'sql_max_Phone')
        #max_Phone = con.get('BASIC', 'normal_uesr')
        #获取最大值加1的tel_phone
        tel_phone = MysqlUtill().get_fetch_one(sql=sql_max_Phone)["MobilePhone"]
        max_phone = str(int(tel_phone) + 1)
        #把最大值tel_phone写入映射类里面
        setattr(Context, 'tel_phone',max_phone)
    # 加 * 号，去掉一层外套
    @data(*excel_date_register)
    #@unpack
    def test_http_case(self,i):
        #对excel里面的正则进行替换
        date = Regular().regular(i.request_data)  # 正则参数替换
        my_log.info('正在执行地{0}条用例; 用例名称:{1}; 用例说明:{2}; 用例接口:{3}'.
                    format(i.case_id, i.case_name, i.case_rept, i.api_name))
        my_log.info('================检查url====================')
        my_log.info('url:{}'.format(config_url+i.url))
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
        res = HttpRequest(config_url+i.url,eval(date),i.mathod)
        my_log.info('实际结果:{}'.format(res.get_text()))
        my_log.info('=================开始断言==================')
        try:
            #断言判断实际结果与期望结果是否一致
            self.assertEqual(json.loads(i.expected_data)['code'],json.loads(res.get_text())['code'])
            Testresult = 'pass'
            if json.loads(res.get_text())['code'] == '10001':  #注册成功，进行数据库校验
                new_phone = MysqlUtill().get_fetch_one(sql=sql_max_Phone)["MobilePhone"]
                if new_phone is not None:
                    self.assertEqual(max_phone,new_phone)
                    my_log.info("数据库校验-->用户{}注册成功".format(new_phone))
                else:
                    raise AssertionError
            else: # 注册失败，进行数据库校验
                new_phone = MysqlUtill().get_fetch_one(sql=sql_max_Phone)["MobilePhone"]
                if new_phone == tel_phone:  # 最新号码等于数据库最新一条数据
                    my_log.info("数据库校验-->注册失败")
                elif new_phone is None:  # 注册第一条数据失败，最新的数据为None
                    my_log.info("数据库校验-->注册失败")
                else:
                    raise AssertionError
        except Exception as e:
            Testresult = 'failed'
            my_log.error('断言错误:{0}'.format(e))
            raise e
        finally:
            my_log.info('resultd的值是:{0}'.format(Testresult))
            my_log.info('=================结束断言==================')
            #写入实际结果actual和result值
            excel_date.write_by_case_id(sheet_name='register', case_id=i.case_id,
                                        actual=res.get_text(), result=Testresult)
    # @classmethod
    # def tearDownClass(cls):
    #     mysql.close()

# if __name__ == '__main__':
#     unittest.main()
