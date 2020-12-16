# -*- coding: utf-8 -*-

import urllib3 
import bs4
from bs4 import BeautifulSoup
import time

import myCSV
import myNeo4j
import myURLcontroller

#下载器
http = urllib3.PoolManager()

#图数据库
movieGDB = myNeo4j.myNeo4j();

#URL管理器
urlManager = myURLcontroller.urlCtrl();


