# -*- coding: utf-8 -*-

import urllib3 
import bs4
from bs4 import BeautifulSoup
import time

import myCSV
import myNeo4j
import myURLcontroller
import myProxy

#下载器
httper = urllib3.PoolManager();

#URL管理器
urlManager = myURLcontroller.urlCtrl();

#代理获取器
proxyPool = myProxy.myProxy("http://stream.singularity-blog.top",5010);

#图数据库
movieGDB = myNeo4j.myNeo4j();


'''
爬取基础的100个页面数据
'''



'''
普通广义爬虫
'''
