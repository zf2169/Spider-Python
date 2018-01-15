#-*- author: Abby Fan -*-
# -*- coding:utf-8 -*-
import chardet
import urllib
from urllib import request
from urllib import parse
from urllib import error
import json
import re

class QSBK:
    def __init__(self):
        self.pageIndex= 1
        self.user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        self.he= {'User-Agent': self.user_agent}
        self.stories= []
        self.enable= False
    
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            req = request.Request(url, headers= self.he)
            res = request.urlopen(req)
            content= res.read().decode('utf-8')
            return content
        except (error.URLError, e):
                if hasattr(e,"reason"):
                    print("Fail to connect the website...", e.reason)
                    return None
                
    def getPageItems(self, pageIndex):
        content= self.getPage(pageIndex)
        if not content:
            print("Fail to load the page...")
            return None
        pattern= re.compile(r'"author clearfix">.*?<h2>(.*?)</h2>.*?'+
                    'class="content">.*?<span>(.*?)</span>.*?'+
                    'gif -->(.*?)<div class="stats">.*?'+
                    'class="stats-vote"><i class="number">(.*?)</i>',
                   re.S)
        items= re.findall(pattern, content)
        pageStories= []
        for i in items:
            haveimg= re.search("img", i[2])
            if not haveimg:
                BR= re.compile(r'<br/>')
                text= re.sub(BR, '\n', i[1])
                pageStories.append([i[0].strip(), text.strip(), i[3].strip()])
        return pageStories
    
    def loadPage(self):
        # if the unread page is less than 2, load the new page
        if self.enable== True:
            if len(self.stories)< 2:
                pageStories= self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex+= 1 
        
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            answer= input()
            self.loadPage()
            if answer == "Q":
                self.enable= False
                return
            print('page:{}\t author:{}\t like:{}\n{}'.format(page, story[0],
                                                                story[2], story[1]))
            
    def start(self):
        print('----------Loading the QSBK successfully----------')
        print('Enter anything to print, Q to quit')
        self.enable= True
        # initially load one page 
        self.loadPage()
        # control which page is reading now
        nowPage=0
        while self.enable:
            if len(self.stories)>0:
                pageStories= self.stories[0]
                nowPage+=1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)
                
spiderqsbk= QSBK()
spiderqsbk.start()