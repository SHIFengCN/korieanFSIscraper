# -*- coding: utf-8 -*-
"""
作者：时锋
更新日期：20170414
版本：1.0
用途：网络爬虫实现韩国食品安全信息的搜集
"""
import sys
import re
from urllib.request import urlopen
#from urllib.error import HTTPError
from bs4 import BeautifulSoup
import urllib
import datetime
import random
import json
import hashlib
import http.client
info = []
def scrap(website):
    print('爬虫开启：', website)
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    #try:
    req = urllib.request.Request(website, headers=hdr)
    try:
        html = urlopen(req)
        bsObj = BeautifulSoup(html)
        #print(bsObj)
    except:
        print('chekandAppend0 error:', website)
        return
    contentList = bsObj.findAll('tr')
    for i in range(len(contentList)):
        if (contentList[i].get_text().find('20') != -1):  # 字段内必须有日期项
            f=open(file='kr.txt',mode='a+',encoding='utf-8')
            krinfo=shrinkblanks(contentList[i].get_text().replace('\r',' ').replace('\n',' '))
            cninfo=translate(krinfo,fromL='kr')
            f.write(cninfo+'\r\n')
            f.close()
    # csvoperation=CsvOperation.CsvOperation()
    # csvoperation.csvnorepeatwritelines(filename,infomations)
#调整递归深度，python默认递归深度不超过1000
#sys.setrecursionlimit(2000)
def shrinkblanks(lines):
    if lines.find('  ')!=-1:
        #需要将lines转换为str，虽然lines本身为str，但是此处不显式声明会出错
        return shrinkblanks(str(lines).replace('  ', ' '))
    return lines

def translate(queryString,fromL,toL='zh'):
    #print('translating:')
    #print(fromL)
    appid = '20170224000039780'
    secretKey = 'OAtEFmWXkAePVKz3h2uA'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q=queryString.replace('\r','').replace('\n',' ')
    #print(q)
    fromLang = fromL
    toLang = toL
    salt = random.randint(32768, 65536)
    #print(salt)
    sign = appid+q+str(salt)+secretKey
    #print(sign)
    m1 = hashlib.md5()
    #print(m1)
    m1.update(sign.encode('utf-8'))
    #print(m1)
    sign = m1.hexdigest()
    #print(sign)
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        dic1=response.read().decode()
        #dic1 = {'type':'dic1','username':'loleina','age':16}
        json_dic1 = json.loads(dic1)
        #print(json_dic1['trans_result'][0]['dst'])
        return json_dic1['trans_result'][0]['dst']
    except:
        print('error:\r\n')
    finally:
        if httpClient:
            httpClient.close()

def doscrap():

    logstr='开始爬取http://www.mfds.go.kr/index.do?mid=664的网页'
    for i in range(191):
        scrap('http://www.mfds.go.kr/index.do?mid=664&pageNo='+str(i+1))
def main():
    doscrap()

if __name__=='__main__':
    main()