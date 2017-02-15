# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 13:41:40 2017

@author: liang.ming
"""

import urllib2
import re
import thread
import time

class Spider_Model:
    
    #初始化
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False
        
        
    def GetPage(self,page):
        myUrl = "http://www.qiushibaike.com/text/page/" + page
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(myUrl, headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        unicodePage = myPage.decode("utf-8")
        myItems = re.findall('\s{3}<span>(.*?)</span>\s{3}', unicodePage, re.S)  
        items = []
        for item in myItems:
            items.append([item.replace("<br/>","")])
        return items

    def LoadPage(self):
        while self.enable:
            if len(self.pages) < 2:
                try:
                    myPage = self.GetPage(str(self.page))
                    self.page += 1
                    self.pages.append(myPage)
                except:
                    print '无法链接糗事百科'
                
            else:
                time.sleep(1)
        
    def ShowPage(self, nowPage, page):
        for items in nowPage:
            print u'第%d页' % page , items[0]
            myInput = raw_input()
            if myInput == "quit":
                self.enable = False
                break
            
    def Start(self):
        self.enable = True
        page = self.page
        
        print u'正在加载请稍候...'
        # 新建一个线程在后台加载段子并存储    
        thread.start_new_thread(self.LoadPage,())
        #----------- 加载处理糗事百科 ----------- 
        while self.enable:
            # 如果self的page数组中存有元素 
            if self.pages:
                nowPage = self.pages[0]
                del self.pages[0]
                self.ShowPage(nowPage,page)
                page += 1
        
#----------- 程序的入口处 -----------          
print u"""  
---------------------------------------  
   程序：糗百爬虫  
   版本：0.1  
   作者：liang.ming
   日期：2017-02-14  
   语言：Python 2.7  
   操作：输入quit退出阅读糗事百科  
   功能：按下回车依次浏览今日的糗百热点  
---------------------------------------  
"""         

print u'请按下回车浏览今日的糗百内容：'
raw_input(' ')
myModel = Spider_Model()
myModel.Start()
        
        
        
        
        
        
        
        
        