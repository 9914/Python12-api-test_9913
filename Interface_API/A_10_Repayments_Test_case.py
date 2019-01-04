#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/15 15:49
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : A_10_Repayments_Test_case.py
# @Software : PyCharm
# @Explain   : 用户回款计划测试用例

from ddt import ddt,data,unpack
from common.http_requests_01 import HttpRequest
from common.http_reading_excel_01 import DoExcel
from common import http_path
from common.Http_config import Reading
from common.http_log import HttpLog
from common.regular_expression import Regular
from common.basic_data import Context
from common.mysql import MysqlUtill
import unittest
import json
from common.common_user import Login
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
#充值
excel_date_generateRepayments = excel_date.get_case('generateRepayments')

@ddt
class HttpCase(Login):
#class HttpCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Login().test_login()    #固定投资用户登录
    def setUp(self):
        global sql,back_plan,Money_back_plan
        sql = con.get("SQL","Money_back_plan")
        Money_back_plan = MysqlUtill().get_fetch_one(sql=sql)
        if Money_back_plan is not None:
            back_plan =Money_back_plan
            print("Money_back_plan:", type(Money_back_plan), Money_back_plan)
        else:
            my_log.info("初始化数据--》回款计划暂未生成！")
    # 加 * 号，去掉一层外套
    @data(*excel_date_generateRepayments)
    def test_http_case(self,i):
        #对excel里面的正则进行替换
        date = Regular().regular(i.request_data)  # 正则参数替换
        my_log.info('正在执行地{0}条用例; 用例名称:{1}; 用例说明:{2}; 用例接口:{3}'.
                    format(i.case_id, i.case_name,i.case_rept,i.api_name))
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
        if hasattr(Context,'cookies'):      #因为第一次登陆没有cookies,需要判断
            cookies = getattr(Context,'cookies')    #存在赋值给cookies
        else:
            cookies = None
        res = HttpRequest(config_url+i.url,json.loads(date),i.mathod,cookies)
        my_log.info('实际结果:{}'.format(res.get_json()))
        # 当cookie不为空时，把cookie写入反射类里面
        if res.get_cookies():
            setattr(Context, 'cookies', res.get_cookies())
        my_log.info('=================开始断言==================')
        try:
            #断言判断实际结果与期望结果是否一致
            self.assertEqual(json.loads(i.expected_data)['code'],json.loads(res.get_text())['code'])
            Testresult = 'pass'
            if json.loads(res.get_text())['msg'] == '生成回款计划成功':  # 生成成功，进行数据库校验
                new_back_plan = MysqlUtill().get_fetch_one(sql=sql)
                try:
                    if Money_back_plan is None and new_back_plan is not None:
                        my_log.info("数据库校验-->回款计划生成成功！")
                    elif Money_back_plan['Id'] < new_back_plan['Id']:
                        my_log.info("数据库校验-->回款计划生成成功！,最新记录ID：{}".format(new_back_plan['Id'] ))
                    elif new_back_plan is None:
                        my_log.info("数据库校验-->回款计划暂未生成！")
                except  Exception as e:
                    my_log.info("数据库校验-->生成回款计划异常{}".format(e))
                    raise e
            else:           #生成失败
                new_back_plan = MysqlUtill().get_fetch_all(sql=sql)
                try:
                    if Money_back_plan['Id'] == new_back_plan['Id']:
                        my_log.info("数据库校验-->生成失败!")
                except Exception as e:
                    my_log.info("数据库校验-->生成失败异常{}".format(e))
                    raise e
        except Exception as e:
            Testresult = 'failed'
            my_log.error('断言错误:{0}'.format(e))
            raise e
        finally:
            my_log.info('resultd的值是:{0}'.format(Testresult))
            my_log.info('=================结束断言==================')
            #写入实际结果actual和result值
            excel_date.write_by_case_id(sheet_name='generateRepayments', case_id=i.case_id,
                                        actual=res.get_text(), result=Testresult)

# if __name__ == '__main__':
#     unittest.main()
