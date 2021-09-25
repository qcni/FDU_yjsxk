# -*- coding: utf-8 -*-
# @Time    : 2021/9/16 8:59
# @Author  : Ni Qingchao

import time
import requests
import ddddocr
import json


def login(username, password):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "yjsxk.fudan.edu.cn",
        "Connection": "keep-alive",
        "Proxy-Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }
    c = requests.post(url='http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/*default/index.do',
                      headers=headers).cookies.get_dict()
    cookie = 'route=' + c['route'] + '; JSESSIONID=' + c['JSESSIONID']
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "yjsxk.fudan.edu.cn",
        "Referer": "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/xsxkHome/gotoChooseCourse.do",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    # headers['Cookie']
    cnt = 0
    while cnt < 5:
        try:
            while True:
                codeUrl = "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/login/4/vcode.do?timestamp={}".format(
                    int(round(time.time() * 1000)))
                vtoken = json.loads(requests.get(url=codeUrl, headers=headers).text)["data"]["token"]
                imgUrl = "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/login/vcode/image.do?vtoken={}".format(
                    vtoken)
                r = requests.get(url=imgUrl, headers=headers)
                ocr = ddddocr.DdddOcr()
                vcode = ocr.classification(r.content)
                if len(vcode) == 4:
                    break

            # with open("moocCode.jpg", "wb", ) as f:
            #     f.write(r.content)

            headers['Content-Length'] = '139'
            headers['Accept'] = "*/*"
            headers['Referer'] = "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/*default/index.do"
            headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            headers['Origin'] = "http://yjsxk.fudan.edu.cn"

            loginUrl = "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/login/check/login.do?timestrap={}".format(
                int(round(time.time() * 1000)))
            data = {
                "loginName": username,
                'loginPwd': password,
                "verifyCode": vcode,
                "vtoken": vtoken
            }
            print(vcode)
            #     print(data)
            time.sleep(2)
            res = requests.post(url=loginUrl, headers=headers, data=data)
            d = res.cookies.get_dict()
            cookie = "_WEU=" + d['_WEU'] + "; " + headers["Cookie"] + "; XK_TOKEN" + d['XK_TOKEN']
            break
        except:
            cnt += 1
            continue
    return cookie


def getCourse(headers):
    url = "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/xsxkCourse/loadGgxxkCourseInfo.do?_={}".format(int(round(time.time() * 1000)))
    data = {
        "query_keyword": "",
        "query_kccc": "",
        "query_syxwlx": "",
        "query_kkyx": "",
        "query_xqdm1": "",
        "query_sfct": "",
        "query_sfym": "",
        "fixedAutoSubmitBug": "",
        "lx": "9",
        "pageIndex": "1",
        "pageSize": "10",
        "sortField": "",
        "sortOrder": ""
    }
    response = requests.post(url=url, headers=headers, data=data)
    json_result = json.loads(response.text)
#     print(json_result)
    return json_result


def choiceCource(courseID, csrfToken, headers):
    url = "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/xsxkCourse/choiceCourse.do?_={}".format(int(round(time.time() * 1000)))
    headers['Content-Length'] = "138"
    data = {
        "bjdm": courseID,
        "lx": "9",
        "bqmc": "公共选修课",
        "csrfToken": csrfToken
    }
    result = requests.post(url=url, headers=headers, data=data)
    return result


def getCsrfToken(Cookie):
    url = "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/xsxkHome/gotoChooseCourse.do"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": Cookie,
        "Host": "yjsxk.fudan.edu.cn",
        "Referer": "http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/*default/index.do",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }
    res = requests.get(url=url, headers=headers).text
    pattern = 'csrfToken'
    index = re.search(pattern, res).span()[1]
    return res[index+9:index+41]


