# -*- coding: utf-8 -*-
# @Time     : 2018/12/15 15:43
# @Author   : Python12_秋
# @Email    : 793630871@qq.com
# @File     : http_request1s.py
# @Software : PyCharm
# @Explain  : Http——Request请求
import json
import requests
class HttpRequest:
    def __init__(self,url,date,method,cookie=None,headers=None):
        try:            #判断请求方式
            if method == 'GET':
                #get 方式，传url地址和参数,指定的资源经服务器端解析后返回响应内容
                self.res = requests.get(url=url, params=date, cookies=cookie, headers=headers)
            elif method == 'POST':
                #post 方式，传url地址，cookis,参数,用于修改服务器上资源的请求
                self.res = requests.post(url=url, data=date, cookies=cookie, headers=headers)
            elif method == 'HEAD':
                # head 方式，传url地址，cookis,参数,用于确认URI的有效性及资源更新的日期时间等
                # 具体来说：1、判断类型；
                # 2、查看响应中的状态码，看对象是否存在（响应：请求执行成功了，但无数据返回）；
                # 3、测试资源是否被修改过
                self.res = requests.head(url=url, data=date, cookies=cookie, headers=headers)
            elif method == 'PUT':
                # put 方式，传url地址，cookis,参数
                #用来传输文件，就像FTP协议的文件上传一样，要求在请求报文的主体中包含文件内容，
                #然后保存在请求URI指定的位置
                self.res = requests.put(url=url, data=date, cookies=cookie, headers=headers)
            elif method == 'DELETE':
                # delete 方式，传url地址，cookis,参数   指明客户端想让服务器删除某个资源
                self.res = requests.delete(url=url, data=date, cookies=cookie, headers=headers)
            elif method == 'OPTIONS':
                # options 方式，传url地址，cookis,参数   查询针对请求URI指定资源支持的方法
                self.res = requests.options(url=url, data=date, cookies=cookie, headers=headers)
        except Exception as e:
            print("requests链接错误:{}".format(e))
            raise e

    def get_statu_code(self):       #返回status_code
        return self.res.status_code

    def get_text(self):            #返回text
        return self.res.text

    def get_json(self):            #返回json
        js = self.res.json()
        res_json = json.dumps(js, ensure_ascii=None, indent=4)
        print("response：",res_json)
        return js
        #return self.res.json

    def get_cookies(self,key = None):           #返回cookies
        if key is not None:
            return self.res.cookies[key]
        else:
            return self.res.cookies

# if __name__ == '__main__':
#     i={'url':'http://test.lemonban.com/futureloan/mvc/api/member/register',
#           'request_data':'{"mobilephone":"15909318312","pwd":"1234567890"}','method':'GET'}
#     m = HttpRequest(i['url'],eval(i['request_data']),str(i['method']))
#     n = m.get_json()
#     l = m.get_text()
#     print(type(n),n)
#     print(type(l),l)
