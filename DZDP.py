#-*- author: Abby Fan -*-
# -*- coding:utf-8 -*-
import chardet
import urllib
from urllib import request
from urllib import parse
from urllib import error
import json
import re
import pandas as pd

class DZDP:
    def __init__(self):
        self.pageIndex= 1
        self.user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        self.he= {'User-Agent': self.user_agent,
                  'Cookie': '_lxsdk_cuid=160900a5378c8-0579da4717c5be-c303767-130980-160900a53783f; _lxsdk=160900a5378c8-0579da4717c5be-c303767-130980-160900a53783f; _hc.v=76ddacc0-0554-3be0-8a19-4e8b5c30cac1.1514245084; aburl=1; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; cy=1; cye=shanghai; s_ViewType=10; _lxsdk_s=160fc19a027-b4e-dd-4ad%7C%7C12',
                  'Accept': 'application/json, text/javascript'}
        self.stories= []
        self.enable= False
        self.out= pd.DataFrame([])
    
    def getPage(self, search, pageIndex):
        try:
            url= 'https://www.dianping.com/search/keyword/1/0_'+ search + '/p'+ str(pageIndex)
            req = request.Request(url, headers= self.he)
            res = request.urlopen(req)
            content= res.read().decode('utf-8')
            return content
        except (error.URLError, e):
                if hasattr(e,"reason"):
                    print("Fail to connect the website...", e.reason)
                    return None
                
    def getPageItems(self, search, pageIndex):
        content= self.getPage(search, pageIndex)
        if not content:
            print("Fail to load the page...")
            return None
        pattern= re.compile(r'class="tit">.*?<h4>(.*?)</h4>.*?'+
                    '"sml-rank-stars.*?title="(.*?)"></span>.*?'+
                    '人均.*?<b>(.*?)</b>.*?'+
                    '<span class="addr">(.*?)</span>',
                   re.S)
        items= re.findall(pattern, content)
        pageStories= []
        for i in items:
            pageStories.append([i[0], i[1], i[2], i[3]])
        return pageStories
    
    def loadPage(self, search):
        # if the unread page is less than 2, load the new page
        if self.enable== True:
            if len(self.stories)< 2:
                pageStories= self.getPageItems(search, self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex+= 1 
            
    def start(self):
        print('----------Loading the DZDP successfully----------')
        print('Enter anything to print, Q to quit')
        self.enable= True
        s= input("What kind of food you want to eat?")
        search= parse.quote(s)
        # initially load one page 
        self.loadPage(search)
        # control which page is reading now
        nowPage=0
        self.loadPage(search)
        while self.enable:        
            answer= input()
            if answer == "Q":
                self.enable= False
                self.out.to_csv('大众点评{}.csv'.format(parse.unquote(search)), 
                                header=True, encoding='utf_8_sig')
                print('The file is exported!')
                return         
            nowPage+=1
            stories= self.getPageItems(search, nowPage)
            self.out= self.out.append(stories)
            print('The page {} is downloaded!'.format(nowPage))
                
spiderdzdp= DZDP()
spiderdzdp.start()