# -*- coding: utf-8 -*-
'''
爬虫程序
'''
import sys
import re
from urllib.request import urlopen
#from urllib.error import HTTPError
from bs4 import BeautifulSoup
import urllib
import datetime
import CsvOperation
class scrap:
    info = []
    def scrap(self,website):
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
            print('chekandAppend0 error:', webname)
            return
        contentList = bsObj.findAll('tr')
        infomations=[]
        for i in range(len(contentList)):
            if (contentList[i].get_text().find('20') != -1):  # 字段内必须有日期项
                infomations.append(self.shrinkblanks(contentList[i].get_text().replace('\r',' ').replace('\n',' ')))
        return infomations
        # csvoperation=CsvOperation.CsvOperation()
        # csvoperation.csvnorepeatwritelines(filename,infomations)
    #调整递归深度，python默认递归深度不超过1000
    #sys.setrecursionlimit(2000)
    def shrinkblanks(self,lines):
        if lines.find('  ')!=-1:
            #需要将lines转换为str，虽然lines本身为str，但是此处不显式声明会出错
            return self.shrinkblanks(str(lines).replace('  ', ' '))
        return lines
