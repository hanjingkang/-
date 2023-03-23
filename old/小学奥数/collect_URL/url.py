import json
import requests
import re

import scrapy_redis

url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzIwNzQ1MzI1Ng==&f=json&offset=10&count=10&is_ok=1&scene=&uin=MTIwMzE5NjA0Mg==&key=40b2857bae2e1f1e44fa2c8d6886f69da0ae62242f50709cbd331105de544fa5639956d5f58ba028ed1c89bfe91f4b178588160892e088cc60f9096c18f2ac7a634a3181ee67f5aa5d74e4a1582613cba6dda85ea3c2c8487db9375ef17bec593ccdfe24b2ccca676bdb0286407625d61384c28366c5d756a5e74b07a2852a8f&pass_ticket=frhexgC9PadKhtbjiSU+mj0RR5Yn4IF+t83IjBX02dsrbQh739fPHOqs5Ai3PDbS&wxtoken=&appmsg_token=1193_5G2GfpRHi8pTBiBOC_2Y7MSaGSkZHbj2HX9o0g~~&x5=0&f=json"

param = {'count': 10, 'offset': 20}
hearder = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6308001b)',
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1203196042; lang=zh_CN; appmsg_token=1193_loYSRPo0kOkRDarOxzkYPTNiHaGe9hz8FK8f_oqMhrUlYOMSW-EaJ-58Re6PjwEosYr7z-i4bZtPgEFo; devicetype=android-29; version=28001e51; pass_ticket=oOfcWis6VziiBzmDP1id9d2eOarAhGaJcS47g/plsGgOmsJlwRCpSoASqXIixYK; wap_sid2=CIqh3b0EEooBeV9IT0xtUkdMY21KOTZHVjlJTk5ab3NVc2xZYWpiYUhVLWxwaFRlazdETjZwblZGZE1PeW00VFVtRE00WWc5WlhKOFpqR3Y3bEFjVVYtSjc2cklTT2dLU01fR0dUN0lfcUJhQk5iVVZJbXBuNTNnajBpM2ZwT1ZFck9PRWVQalFiMEk0WVNBQUF+MLmG/JsGOA1AlU4=;wxtokenkey=777;wxuin=1203196042',
    'Host': 'mp.weixin.qq.com',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}

t = requests.get(url=url, headers=hearder)
t=json.loads(t.json()['general_msg_list'])

urllist=[]

""" with open(r"C:/Users/Han JingKang/Desktop/分布式爬虫/小学奥数/temp/tmp.json", 'w', encoding="utf-8") as f:
    f.write(t) """


for i in t['list']:
    if("1--6年级" in i['app_msg_ext_info']['title']):
        urllist.append(i['app_msg_ext_info']['content_url'])
    for  j in i['app_msg_ext_info']['multi_app_msg_item_list']:
        if("1--6年级"  in j['title']):
            urllist.append(j['content_url'])

print(len(urllist))
print(urllist)

