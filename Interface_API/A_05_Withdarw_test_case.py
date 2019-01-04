#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/15 15:49
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : A_05_Withdarw_test_case.py
# @Software : PyCharm
# @Explain  : 提现测试用例

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
#提现
excel_date_withdarw = excel_date.get_case('withdarw')

@ddt
class HttpCase(unittest.TestCase):
    def setUp(self):
        self.sql = con.get('SQL','Pay_LeaveAmount')
        #充值之前的账户余额
        self.LeaveAmount = MysqlUtill().get_fetch_one(sql=self.sql)
        try:
            if self.LeaveAmount["LeaveAmount"] == 0:
                my_log.info("初始化数据--》账户余额为0 ，不允许提现，请先充值！")
            else:
                my_log.info("初始化数据--》提现前账户余额:{}".format(self.LeaveAmount["LeaveAmount"]))
        except Exception as e:
            my_log.info("初始化数据--》账户金额异常：{}".format(e))
            raise e
        #借款人提现流水记录
        self.sq = con.get('SQL','normal_record')
        self.Pay_record = MysqlUtill().get_fetch_one(sql=self.sq)
        my_log.info("初始化数据--》没有提现之前最新的一条流水记录：{}".format(self.Pay_record))
    # 加 * 号，去掉一层外套
    @data(*excel_date_withdarw)
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
        if hasattr(Context, 'cookies'):  # 因为第一次登陆没有cookies,需要判断
            cookies = getattr(Context, 'cookies')  # 存在赋值给cookies
        else:
            cookies = None
        res = HttpRequest(config_url+i.url,json.loads(date),i.mathod,cookies)
        my_log.info('实际结果:{}'.format(res.get_json()))
        # 当cookie不为空时,写用映射文件Context里面
        if res.get_cookies():
            setattr(Context, 'cookies', res.get_cookies())
        my_log.info('=================开始断言==================')
        try:
            #断言判断实际结果与期望结果是否一致
            self.assertEqual(json.loads(i.expected_data)['code'],json.loads(res.get_text())['code'])
            Testresult = 'pass'
            if json.loads(res.get_text())['code'] == '10001':  # 提现成功，进行数据库校验
                # 把提现成功的金额写入映射Context里面
                if 'amount' not in eval(date):  # 如果在date里面没有amount字段，直接赋值为0
                    setattr(Context, "leaveamount", 0)
                else:
                    setattr(Context, "leaveamount", eval(date)["amount"])
                Amount = MysqlUtill().get_fetch_one(sql=self.sql)       #获取最新的余额
                amount = getattr(Context, "leaveamount")     #读取反射里面充值成功的金额
                # 余额 = 初始金额-提现金额
                money = int(self.LeaveAmount["LeaveAmount"]) - int(amount)
                try:
                    self.assertEqual(int(Amount["LeaveAmount"]), money)     #判断余额是否正确
                    my_log.info("数据库校验-->提现成功后账户余额:{}".format(Amount["LeaveAmount"]))
                except BaseException as b:
                    my_log.info("数据库校验-->提现异常：{}".format(b))
                    raise b
                #查询提现成功流水记录
                new_recod = MysqlUtill().get_fetch_one(sql=self.sq)
                if self.Pay_record is None:
                    my_log.info('数据库校验-->用户无流水记录')
                else:
                    if self.Pay_record['Id'] == new_recod['Id']:
                        my_log.info('数据库校验-->没有进行提现操作')
                    elif new_recod['Id'] > self.Pay_record['Id']:
                        my_log.info('数据库校验-->提现成功，流水记录ID是{}'.format(new_recod['Id']))
                    else:
                        raise AssertionError
            else:
                try:  # 提现失败，进行数据库校验
                    mou = MysqlUtill().get_fetch_one(sql=self.sql)  # 获取最新的余额
                    self.assertEqual(int(self.LeaveAmount["LeaveAmount"]), int(mou["LeaveAmount"]))  # 判断余额是否正确
                    my_log.info("数据库校验-->提现失败账户余额:{}".format(mou["LeaveAmount"]))
                except Exception as e:
                    my_log.info("数据库校验-->提现异常：{}".format(e))
                    raise e
                # 查询提现成功流水记录
                new_recod = MysqlUtill().get_fetch_one(sql=self.sq)
                if self.Pay_record == None:
                    my_log.info('数据库校验-->提现失败,新用户未充值，进行提现，请先充值')
                else:
                    if self.Pay_record['Id'] == new_recod['Id']:
                        my_log.info('数据库校验-->提现失败')
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
            excel_date.write_by_case_id(sheet_name='withdarw', case_id=i.case_id,
                                        actual=res.get_text(), result=Testresult)


if __name__ == '__main__':
    unittest.main()
