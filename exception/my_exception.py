#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/16 20:15
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : my_exception.py
# @Software : PyCharm

class MyException:
    def my_exception_test(self):
        pass
statu = [1, 2, 3]
new_status = [1,2, 3, 4, 8]
for i in range(0, len(statu)):
    i = i+1
    for j in range(i, len(new_status),1):
        print('审核成功，状态为：{0}'.format(new_status[j]))
    print("-"*20)



