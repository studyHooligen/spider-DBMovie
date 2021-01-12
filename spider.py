# -*- coding: utf-8 -*-

import urllib3 
import bs4
from bs4 import BeautifulSoup
import time
import re

import myCSV
import myNeo4j
import myURLcontroller
import myProxy

'''
用户参数配置
'''
LIMIT_OBEJECT = 100     # 闲置爬取的数据量，单位：个电影

LIMIT_RATE = 3          # 爬虫速率

USE_PROXY = False       # 选择是否使用代理服务

CLEAN_ORIGINAL_DATABASE = True # 爬虫开始前删除原始数据库数据

SAVE_HTMLFILE = True    # 是否保存爬取过程中的HTML页面内容
SAVE2CSV = True         # 是否把爬取的数据存储到本地csv文件中
'''
用户参数配置完毕
'''

# 获取运行时间
RUNNING_TIME = time.strftime('%Y-%m-%d,%H:%m',time.localtime(time.time()))

#下载器
downloader = urllib3.PoolManager();

#URL管理器
urlManager = myURLcontroller.urlCtrl();

#代理获取器
proxyPool = myProxy.myProxy("http://stream.singularity-blog.top",5010);

#图数据库
GDB_movie = myNeo4j.myNeo4j();

#CSV读写器
if SAVE2CSV:
    movieBrief_csvWriter = myCSV.myCSV("./csvData/movieBrief"+RUNNING_TIME+".csv","wb","utf-8")

    movieBrief_csvWriter.writerow(["电影名字",
                                   "电影原名",
                                   "其他名字",
                                   "详细内容链接",
                                   "导演",
                                   "编剧",
                                   "主演",
                                   "年份",
                                   "电影类型",
                                   "国家/地区",
                                   "语言",
                                   "上映日期",
                                   "片长"
                                   ])

if CLEAN_ORIGINAL_DATABASE:
    GDB_movie.cleanDatabase()

'''
爬取基础的250个页面数据到url数据器里
'''

print('''-------开始爬取根数据--------''')
urlRoot = "https://movie.douban.com/top250?start="  # 根爬取地址

pageNum = 0 #遍历用的页面号
while pageNum < 10:
    
    urlNow = urlRoot + str(pageNum*25)    #当前要爬的路径
    
    r = downloader.request('GET',urlNow)  #下载HTML数据
    
    if(r.status != 200):    #检测是否请求失败（被豆瓣查水表）
        print("get error,status code:",str(r.status))
        exit(-1)
    
    pageNum += 1    #迭代
    
    '''
    存储网页原HTML数据
    用户可配置开启
    '''
    if SAVE_HTMLFILE:
        localSaveFile = open("./sourceHTMl/top250Main/豆瓣电影top250-"+str(pageNum)+".html",mode = "wb")
        
        localSaveFile.write(r.data) #存储网页数据
        
        localSaveFile.close()   #关闭文件
    
    '''
    开始分析网页文件
    '''
    wholeHTML_bsObj = BeautifulSoup(r.data,"html.parser",from_encoding="utf-8")
    
    mainGrid = wholeHTML_bsObj.find("ol",class_ = "grid_view")
    
    movieBrief_list = mainGrid.find_all("li")
    
    for movie in movieBrief_list:
        
        movieName = movie.find_all("span",class_ = "title")   #查电影的名字
        movieOtherName = movie.find("span",class_ = "other")    #查电影的其他名字
        movieLink = movie.find('a').attrs['href'] #电影详细内容链接
        
        #防止电影没有第二名字
        movieName.append(movieName[0])
        
        # if SAVE2CSV:    # 存储数据到CSV文件
        #     movieBrief_csvWriter.writerow([movieName[0].text.replace(u'\xa0', u' '),
        #                                    movieName[1].text.replace(u'\xa0', u' ').replace(" / ",''),
        #                                    movieOtherName.text.replace(u'\xa0', u' ').replace(" / ",' '),
        #                                    movieLink
        #                                    ])
        
        # 电影名字字符格式调整
        movieName[0] = movieName[0].text.replace(u'\xa0', u' ');
        movieName[1] = movieName[1].text.replace(u'\xa0', u' ').replace(" / ",'');
        
        # 存储数据到知识图谱库
        # GDB_movie.add_Movie(movieName[0],
        #                    movieName[1],
        #                    movieOtherName.text.replace(u'\xa0', u' ').replace(" / ",' '),
        #                    movieLink
        #                    )
        
        # 存储页面链接到（广义爬虫）URL管理器中
        urlManager.add_URL(movieLink,movieName[0])
    
    '''
    防止查水表，适当限速
    '''
    time.sleep(LIMIT_RATE)
    
    print("爬取了第"+str(pageNum)+"次根数据")
    
print("top250主页面数据爬取完成")



'''
普通广义爬虫
'''
pageNum = 0

while LIMIT_OBEJECT > pageNum:
    
    '''循环迭代'''
    pageNum += 1;   # 迭代
    print("-----正在爬取第"+str(pageNum)+"次页面数据-----")
    
    if urlManager.empty():
        break;
    movieNow = urlManager.get_URL()   #获取当前爬取页面的URL
    urlNow = movieNow[1];
    name = movieNow[0];
    
    '''从网站下载数据'''
    time.sleep(LIMIT_RATE)  # 限速
    r = downloader.request('GET',urlNow)  #下载HTML数据
    
    
    '''
    开始分析页面
    '''
    wholeHTML_bsObj = BeautifulSoup(r.data,"html.parser",from_encoding="utf-8")
    
    # 年份数据
    year = wholeHTML_bsObj.find("span",class_ = "year").text.replace('(','').replace(')','')
    
    #电影详细数据块提取
    infoDiv = wholeHTML_bsObj.find("div",id = "info")
    
    #电影主要人物数据提取：导演、编剧、主演
    mainAttrList = infoDiv.find_all("span",class_ = "attrs")
    director = mainAttrList[0].text     # 导演
    directorLink = mainAttrList[0].find('a').attrs['href'];   # 导演页面链接
    scriptwriter = mainAttrList[1].text # 编剧
    leadRoleA = mainAttrList[2].find_all("a") # 主演提取
    leadRoleList = []
    for i in leadRoleA:
        # 主演数据格式转换，转为元组对：（主演名字+主演页面链接）
        leadRoleList.append((i.text,i.attrs['href']))
    
    #电影类型提取
    genre = infoDiv.find_all("span",property = "v:genre")
    genreList = [];
    for i in genre: # 格式转换
        genreList.append(i.text)
    #国家
    matchCountry = re.search( r'制片国家/地区:.*\n', infoDiv.text, re.M|re.I)
    country = matchCountry.group().replace("制片国家/地区:",'').replace("\n",'').replace(" ",'')
    #语言
    matchLanguage = re.search( r'语言:.*\n', infoDiv.text, re.M|re.I)
    language = matchLanguage.group().replace("语言:",'').replace("\n",'').replace(" ",'')
    #上映日期
    releaseDataRes = infoDiv.find_all("span",property = "v:initialReleaseDate")
    releaseDataList = []
    for i in releaseDataRes:   # 格式转换
        releaseDataList.append(i.text)
    #片长
    movieLength = infoDiv.find("span",property = "v:runtime").text
    # 其他名字
    
    matchOtherName = re.search(r'又名:.*\n', infoDiv.text, re.M|re.I)
    if matchOtherName is None:
        matchOtherName = '';
        otherName = '';
    else:
        otherName = matchOtherName.group().replace("又名:",'').replace("\n",'').replace(" ",'')
    
    
    '''开始导入数据至图数据库'''
    GDB_movie.add_Movie(movieName = name,
                        originalName = name,
                        otherName = otherName,
                        infPageLink = urlNow,
                        country = country,
                        year = int(year),
                        date = str(releaseDataList),
                        length = movieLength
                        )   # 添加电影至数据库
    
    for i in leadRoleList:
        GDB_movie.add_actor(name = i[0],
                            originalName = i[0],
                            link = i[1]);   # 添加演员
        GDB_movie.establishRelation_actor2movie(i[0],name); # 建立关系
        
    for i in genreList:
        GDB_movie.add_movieType(i); # 添加电影类型
        GDB_movie.establishRelation_movie2type(name,i); # 建立关系
    
    GDB_movie.add_director(director,directorLink); # 添加导演
    GDB_movie.establishRelation_director2movie(director,name); # 建立导演关系
    
    GDB_movie.add_scriptwriter(scriptwriter);   # 添加编剧
    GDB_movie.establishRelation_srcriptWriter2movie(scriptwriter,name); # 添加编剧关系
    
    
    
    '''保存数据至本地'''
    if SAVE2CSV:
        movieBrief_csvWriter.writerow([name,        # 电影名字
                                       name,        # 电影原名
                                       otherName,   # 其他名字
                                       urlNow,      # 电影页面链接
                                       director,    # 导演
                                       scriptwriter,        # 编剧
                                       str(leadRoleList),   # 主演
                                       year,                # 年份
                                       str(genreList),      # 类别
                                       country,             # 国家
                                       language,            # 语言
                                       str(releaseDataList),# 发行上映日期
                                       str(movieLength)     # 电影长度
                                    ])
        
    '''更新URL管理器新数据（有待测试）'''
    # 电影推荐数据块提取
    recmDiv = wholeHTML_bsObj.find("div",id = "recommendations")
    recmMovieFind = recmDiv.find_all("dd");
    # 提取当前页面可爬的URL
    recmMovieList = [];
    for i in recmMovieFind:
        recmMovieList.append((i.find('a').text,i.find('a').attrs['href']))
    #判断找到的新页面是否已经爬过了，如果爬过则跳过
    for i in recmMovieList:
        if len(GDB_movie.search_Movie(i[0])) == 0:    # 查看是否爬过了
            urlManager.add_URL(i)   # 添加到URL管理器中
            

    print("完成爬取第"+str(pageNum)+"次页面数据")
'''
程序退出前收尾工作
'''
print("爬虫运行完成，共爬取电影数据："+str(pageNum)+"条。");
print("------------正在退出程序--------------");

if SAVE2CSV:    # 关闭CSV读写器
    del movieBrief_csvWriter

print("bye~")
