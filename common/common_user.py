"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2019/1/3 16:23
# @Author    : Python12_9913_秋     
# @Email     : 793630871@qq.com    
# @File      : common_user             
# @Software  : PyCharm    
# @User      ：skw             
# @Project   ：Python12-api-test_9913      
# @Explain   : 登录账户
"""
from common.http_requests_01 import HttpRequest
from common.basic_data import Context
import unittest
class Login(unittest.TestCase):
    def test_login(self):
        url = 'http://test.lemonban.com/futureloan/mvc/api/member/login'
        method = 'GET'
        date = {"mobilephone": "15909318312", "pwd": "1234567890"}
        re = HttpRequest(url=url,date=date,method=method)
        setattr(Context,'cookies',re.get_cookies())
        print(re.get_statu_code())

# if __name__ == '__main__':
#     l = Login()
#     m = l.setUpClass()
#     print(m)