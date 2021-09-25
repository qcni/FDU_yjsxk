# -*- coding: utf-8 -*-
# @Time    : 2021/9/16 8:59
# @Author  : Ni Qingchao

import time
import requests
import json
import ddddocr
import re
import itchat
from utils import *

def main(username, pwd, un=0):

    print('休眠中')
    #     time.sleep(3600*4) # 设置休眠时间
    print('开始抢课')
    if un:
        itchat.send('开始运行啦', toUserName=un)

    Cookie = login(username, pwd)
    print('登录成功')
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "160",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "yjsxk.fudan.edu.cn",
        "Origin": "http://yjsxk.fudan.edu.cn",
        "Cookie": Cookie,
        "Proxy-Connection": "keep-alive",
        "Referer": "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/xsxkHome/gotoChooseCourse.do",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    count = 1
    while count < 10000:
        print(count)
        data = getCourse(headers)['datas']
        if data[20]['WID'] == 'c5de2b503b784a88ab939a6d5caa01dd':
            ymq = data[20]
        else:
            for item in data:
                if item['WID'] == 'c5de2b503b784a88ab939a6d5caa01dd':
                    ymq = item
                    break
        print(ymq['RKJS'],id(ymq))
        if ymq['KXRS'] > ymq['DQRS']:
            try:
                if un:
                    itchat.send('有余量了，快去抢', toUserName=un)
            except:
                pass
            finally:
                Cookie = headers['Cookie']
                csrfToken = getCsrfToken(Cookie)
                print(csrfToken)
                response = choiceCource(courseID=ymq['BJDM'], csrfToken=csrfToken, headers=headers)
                print(response.text)
                break
        time.sleep(30)
        count += 1


if __name__ == "__main__":
    username = "*******"#"你的学号"
    pwd = "*********" #加密后的密码" 可通过网页检查获取
    send_message = False # 默认给微信发送信息
    if send_message:
        itchat.auto_login()
        un = 'filehelper' # 默认给文件传输助手发送提醒
        un = itchat.search_friends(name=u'。。')[0]["UserName"]
    else:
        un = 0
    while True:
        try:
            main(username, pwd, un)
            break
        except json.decoder.JSONDecodeError:
            continue