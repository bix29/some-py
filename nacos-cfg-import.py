# coding:utf-8

import os
import sys
import requests

base_url = 'http://192.168.56.101:8848/nacos/v1' # nacos server

if len(sys.argv) != 2:
    print("参数错误。")
    print("usage: " + str(sys.argv[0]) + " <url of config-file.zip>")
    exit(1)

cfg_file_url=str(sys.argv[1])
cfg_file_name=os.path.split(cfg_file_url)[1]

#print(cfg_file_name)

login_url = base_url + "/auth/login"

h = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive"
}

login_body = {
       "username":"nacos",
       "password":"nacos1"
}

s = requests.session() 
r = s.post(login_url, data=login_body, headers=h)
# print(r.content)
## nacos 1.1.0 存在 bug, 及时登录失败或者不登录，也能上传配置文件

import_url = base_url + "/cs/configs?import=true&namespace=" 
import_body = {"policy": "OVERWRITE"}
# import_file = {"file": (cfg_file_name, open(cfg_file_url, "rb"), "application/zip")}
import_file = {"file": (cfg_file_name, requests.get(cfg_file_url).content, "application/zip")}
r = s.post(import_url, data=import_body, files=import_file)
print(r.content)
