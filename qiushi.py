# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

class qsbk:
    def __init__(self):
        self.pageIndex = 1
        #初始化headers
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        self.headers = {'User-Agent':self.user_agent}
        #初始化段子变量
        self.stories = []
        #初始化程序开关
        self.enable = False

    #传入页面
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/'+str(pageIndex)
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print e.reason
                return None

    #传入页面代码，筛选文字段落
    def getPageItems(self,pageIndex):
        print 'getPageItems'
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print '页面加载失败...'
            return None
        pattern = re.compile('<div class="author clearfix">.*?href.*?<img src.*?title=.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>.*?<i class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,'\n',item[1])
            pageStories.append([item[0],text,item[2]])
        return pageStories

    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        print 'LoadOage'
        if len(self.stories) < 2:
            pageStories = self.getPageItems(self.pageIndex)
            if pageStories:
                self.stories.append(pageStories)
                self.pageIndex += 1

    #控制每次打印输出一次
    def getOneStory(self,pageStories,page):
        print 'getOneStory'
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t赞:%s\n%s" %(page,story[0],story[2],story[1])

    #开始方法
    def start(self):
        print u'正在读取丑事百科，按回车查看新消息，q退出'
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            print 'start'
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)

spider = qsbk()
spider.start()