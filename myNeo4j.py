# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 16:27:43 2020

@author: 23731
"""

import neo4j
from neo4j import (GraphDatabase, WRITE_ACCESS, unit_of_work)

class myNeo4j:
    def __init__(self, 
                 url = "neo4j://localhost:7687", 
                 userName = "neo4j", 
                 password = "1234567890"):
        '''
        创建一个neo4j图数据库操作对象
        
        Parameters
        ----------
        url : str
            数据库路径，默认为本地的7687端口路径
        userName : str
            登陆用户名
        password : str
            登陆密码

        Returns
        -------
        None.

        '''
        self.driver = GraphDatabase.driver(url, auth=(userName,password))

    def __del__(self):
        '''
        对象析构函数

        Returns
        -------
        None.

        '''
        self.driver.close()
    
    
    def add_Movie(self,
                  movieName,
                  originalName = '', otherName = '',
                  infPageLink = ''):
        '''
        

        Parameters
        ----------
        movieName : str
            电影名字.
        originalName : str
            电影原名.
        otherName : str
            其他名字.
        infPageLink : str
            电影内容页面链接

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
                
        def __create_movieNode(tx, movieName,originalName,otherName,infPageLink):
            return tx.run('''CREATE (
                            a:movie 
                            {
                            name: $name, 
                            origName: $origName, 
                            otherName: $otherName,
                            link: $link
                            }
                            ) RETURN id(a)''',
                            name=movieName,
                            origName = originalName,
                            otherName = otherName,
                            link = infPageLink
                            ).single().value()
        
        with self.driver.session() as session:
            return session.write_transaction(__create_movieNode,
                                             movieName,
                                             originalName,
                                             otherName,
                                             infPageLink);
    def cleanDatabase(self):
        '''
        清空数据库里面的所有数据

        Returns
        -------
        None.

        '''
        def __cleanRelation(tx):
            return tx.run('''MATCH (n)-[r]->(m) DELETE r''')
        
        def __cleanNode(tx):
            return tx.run('''MATCH (n) DELETE n''')
        
        with self.driver.session() as session:
            # session.write_transaction(__cleanRelation);
            session.write_transaction(__cleanNode);
            
if __name__ == "__main__":
    neoObj = myNeo4j();
    