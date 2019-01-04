#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/15 15:49
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : A_09_Bidloan_test_case.py
# @Software : PyCharm
# @Explain  : 竞标接口测试用例

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
#竞标
excel_date_bidLoan = excel_date.get_case('bidLoan')

@ddt
class HttpCase(Login):
#class HttpCase(unittest.TestCase):
#金额：购买用户减少，项目账户增加
#购买用户的流水记录
#投资记录
#项目金额减少
    @classmethod
    def setUpClass(cls):
        Login().test_login()    #固定投资用户登录
    def setUp(self):
        global sql1,sql2,sql3,sql4,sql5,meny,mount,poject_Amount,normal_record,Income_record,record_all
        # 借款人用户金额
        sql1 = con.get("SQL","Pay_LeaveAmount")
        meny = MysqlUtill().get_fetch_one(sql=sql1)
        my_log.info("初始化数据--》借款人账户余额为:{}".format(meny["LeaveAmount"]))
        print(type(meny), meny)
        # 投资人用户金额
        sql2 = con.get("SQL", "Income_LeaveAmount")
        mount = MysqlUtill().get_fetch_one(sql=sql2)
        print(type(mount), mount)
        try:
            if mount["LeaveAmount"] == 0:
                my_log.info("初始化数据--》投资人账户余额为0 ，不允许投资，请先充值！")
            else:
                my_log.info("初始化数据--》投资人账户余额为:{}".format(mount["LeaveAmount"]))
        except Exception as e:
            my_log.info("初始化数据--》投资人账户金额异常：{}".format(e))
            raise e
        # 标的金额
        sql3 = con.get("SQL","poject_Amount")
        poject_Amount = MysqlUtill().get_fetch_one(sql=sql3)
        print(type(poject_Amount),poject_Amount)
        # 借款人用户流水记录
        sql4 = con.get("SQL","normal_record")
        normal_record = MysqlUtill().get_fetch_one(sql=sql4)
        # 投资人用户流水记录
        sql5 = con.get("SQL", "Income_record")
        Income_record = MysqlUtill().get_fetch_one(sql=sql5)
        #对当前项目的投资记录
        sql6 = con.get("SQL", "Investment_record_all")
        record_all = MysqlUtill().get_fetch_all(sql=sql6)

    # 加 * 号，去掉一层外套
    @data(*excel_date_bidLoan)
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
        if hasattr(Context,'cookies'):      #因为第一次登陆没有cookies,需要判断
            cookies = getattr(Context,'cookies')    #存在赋值给cookies
        else:
            cookies = None
        res = HttpRequest(config_url+i.url,json.loads(date),i.mathod,cookies)
        my_log.info('实际结果:{}'.format(res.get_json()))
        # 当cookie不为空时，把cookie写入反射类里面
        if res.get_cookies():
            setattr(Context,'cookies',res.get_cookies())
        my_log.info('=================开始断言==================')
        try:
            #断言判断实际结果与期望结果是否一致
            self.assertEqual(json.loads(i.expected_data)['code'],json.loads(res.get_text())['code'])
            Testresult = 'pass'
            if json.loads(res.get_text())['code'] == '10001':  # 充值成功，进行数据库校验
                # 把竞标成功的金额写入映射Context里面
                if 'amount' not in eval(date):  # 如果在date里面没有amount字段，直接赋值为0
                    setattr(Context, "leaveamount", 0)
                else:
                    setattr(Context, "leaveamount", eval(date)["amount"])
                re_amount = getattr(Context, "leaveamount")  # 读取反射里面竞标成功的金额
                #标的最新的金额
                # new_poject_Amount = MysqlUtill().get_fetch_one(sql=sql3)
                # po_Amount = int(poject_Amount["Amount"]) - int(re_amount)
                # try:
                #     if new_poject_Amount == '0':
                #         my_log.info("数据库校验-->已满标")
                #     else:
                #         self.assertEqual(int(new_poject_Amount["Amount"]), po_Amount)
                #         my_log.info("数据库校验-->最新可竞标的余额:{}".format(new_poject_Amount["Amount"]))
                # except BaseException as b:
                #     my_log.info("数据库校验-->竞标余额异常：{}".format(b))
                #     raise b
                #借款人
                # new_meny = MysqlUtill().get_fetch_one(sql=sql1)
                # ne_men = int(meny["LeaveAmount"]) + int(re_amount)
                # try:
                #     self.assertEqual(int(new_meny["LeaveAmount"]), ne_men)
                #     my_log.info("数据库校验-->借款人的最新余额:{}".format(new_meny["LeaveAmount"]))
                # except BaseException as b:
                #     my_log.info("数据库校验-->借款人余额异常：{}".format(b))
                #     raise b
                #投资人
                new_mount = MysqlUtill().get_fetch_one(sql=sql2)
                ne_moun = float(mount["LeaveAmount"]) - float(re_amount["LeaveAmount"])
                try:
                    self.assertEqual(float(new_mount["LeaveAmount"]), ne_moun)  # 判断余额是否正确
                    my_log.info("数据库校验-->投资人的最新余额:{}".format(new_mount["LeaveAmount"]))
                except BaseException as b:
                    my_log.info("数据库校验-->投资人余额异常：{}".format(b))
                    raise b
                # 把借款人的流水记录
                new_normal_record = MysqlUtill().get_fetch_one(sql=sql4)
                if normal_record is None:
                    my_log.info('数据库校验-->借款人未充值、提现，没有流水记录！')
                else:
                    if normal_record['Id'] == new_normal_record['Id']:
                        my_log.info('数据库校验-->借款人没有进行提现操作')
                    elif new_normal_record['Id'] > normal_record['Id']:
                        my_log.info('数据库校验-->借款人提现操作成功，流水记录ID是{}'.format(new_normal_record['Id']))
                    else:
                        raise AssertionError
                # 把投资人投资记录
                new_Income_record = MysqlUtill().get_fetch_one(sql=sql4)
                if Income_record is None:
                    my_log.info('数据库校验-->投资人第一次投标')
                else:
                    if Income_record['Id'] == new_Income_record['Id']:
                        my_log.info('数据库校验-->投资人没有进行提现操作')
                    elif new_Income_record['Id'] > Income_record['Id']:
                        my_log.info('数据库校验-->投资人提现操作成功，流水记录ID是{}'.format(new_Income_record['Id']))
                    else:
                        raise AssertionError
            else:   #竞标失败，数据校验
                new_poject_Amount = MysqlUtill().get_fetch_one(sql=sql3)  # 最新的竞标金额
                try:
                    self.assertEqual(int(poject_Amount["Amount"]), new_poject_Amount["Amount"])
                    my_log.info("数据库校验-->最新可竞标的余额:{}".format(poject_Amount["Amount"]))
                except BaseException as b:
                    my_log.info("数据库校验-->竞标余额异常：{}".format(b))
                    raise b
                # 借款人
                new_meny = MysqlUtill().get_fetch_one(sql=sql1)
                try:
                    self.assertEqual(int(meny["LeaveAmount"]), new_meny["LeaveAmount"])
                    my_log.info("数据库校验-->借款人的最新余额:{}".format(new_meny["LeaveAmount"]))
                except BaseException as b:
                    my_log.info("数据库校验-->借款人余额异常：{}".format(b))
                    raise b
                # 投资人
                new_mount = MysqlUtill().get_fetch_one(sql=sql2)
                try:
                    self.assertEqual(int(mount["LeaveAmount"]), new_mount["LeaveAmount"])  # 判断余额是否正确
                    my_log.info("数据库校验-->投资人的最新余额:{}".format(new_mount["LeaveAmount"]))
                except BaseException as b:
                    my_log.info("数据库校验-->投资人余额异常：{}".format(b))
                    raise b
                #把借款人的流水记录
                new_normal_record = MysqlUtill().get_fetch_one(sql=sql4)
                if normal_record is None:
                    my_log.info('数据库校验-->借款人未充值、提现，没有流水记录！')
                else:
                    if normal_record['Id'] == new_normal_record['Id']:
                        my_log.info('数据库校验-->借款人最新流水记录{}'.format(new_normal_record['Id']))
                    else:
                        raise AssertionError
                # 投资人投资记录
                new_Income_record = MysqlUtill().get_fetch_one(sql=sql4)
                if Income_record is None:
                    my_log.info('数据库校验-->投资人第一次投标')
                else:
                    if Income_record['Id'] == new_Income_record['Id']:
                        my_log.info('数据库校验-->投资人最新流水记录{}'.format(new_Income_record['Id']))
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
            excel_date.write_by_case_id(sheet_name='bidLoan', case_id=i.case_id,
                                        actual=res.get_text(), result=Testresult)

# if __name__ == '__main__':
#     unittest.main()
# 金额为小数时，如何避免重复判断