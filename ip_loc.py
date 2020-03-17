# coding=utf-8

import sys
import requests
import json
from lxml import etree
import re


from workflow import Workflow3

def check_ip(ipAddr):
    compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True    
    else:    
        return False

def main(wf):
    if wf.args[0] == '192.168.0.1' or wf.args[0] == '192.168.1.1':
        wf.add_item('No support this ip')
        wf.send_feedback()
        return
    if not check_ip(wf.args[0]):
        wf.add_item('Is not a ip address, please input a legal ip.')
        wf.send_feedback()
        return

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,fr;q=0.6", "Cache-Control": "no-cache", "Connection": "keep-alive",
               "Cookie": "Hm_lvt_f4f76646cd877e538aa1fbbdf351c548=1582275897,1582450903; ASPSESSIONIDAARSQDDB=AICAKJIDEODCNLPIFCHMMLJG; Hm_lvt_b018ba5033f3b0d184416653ad858a48=1584413757; Hm_lvt_f4f76646cd877e538aa1fbbdf351c548=1582275897,1582450903,1584426261; Hm_lpvt_f4f76646cd877e538aa1fbbdf351c548=1584426261; PHPSESSID=oft8o3mu8tvtd1mutsqmls1mg5; Hm_lpvt_b018ba5033f3b0d184416653ad858a48=1584426559",
               "Host": "www.ip138.com", "Pragma": "no-cache", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1",
               "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
    r = requests.get('https://www.ip138.com/iplookup.asp?ip=%s&action=2' % wf.args[0], headers=headers)
    
    if r.status_code != 200:
        wf.add_item('request error, code is %s!' % r.status_code)
        wf.send_feedback()
        return

    r.encoding = 'gb2312'
    html = etree.HTML(r.text)
    query_string = html.xpath('//h1')[0].xpath('string(.)').strip()
    result1 = html.xpath('//li')[0].xpath('string(.)').strip()
    result2 = html.xpath('//li')[1].xpath('string(.)').strip()
    result3 = html.xpath('//li')[2].xpath('string(.)').strip()
    result4 = html.xpath('//li')[3].xpath('string(.)').strip()
    result5 = html.xpath('//li')[4].xpath('string(.)').strip()
    wf.add_item(query_string.encode('utf-8'))
    wf.add_item(result1.encode('utf-8'))
    wf.add_item(result2.encode('utf-8'))
    wf.add_item(result3.encode('utf-8'))
    wf.add_item(result4.encode('utf-8'))
    wf.add_item(result5.encode('utf-8'))
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
