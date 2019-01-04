#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/15 18:29
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : Prospect_Loan_API_Interface_Report.py
# @Software : PyCharm
# @Explain  : 测试报告
import unittest
from common import http_path
import HTMLTestRunnerNew

discover = unittest.defaultTestLoader.discover(http_path.test_path,pattern='*_test_case*',top_level_dir=None)
with open(http_path.reprot_path,'wb+') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(file, title='前程贷API接口测试报告', tester='Python12_9913_秋')
    runner.run(discover)
