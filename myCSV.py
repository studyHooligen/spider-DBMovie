# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 19:37:47 2020

@author: 江榕煜
"""


class myCSV:
    '''
    这是一个非标准库的csv写入包
    '''
    def __init__(self,fileAddr,fileOperateType = "wb",encoding = "utf-8"):
        '''
        创建一个CSV文件写入对象

        Parameters
        ----------
        fileAddr : str
            文件路径字符串
        fileOperateType : str
            文件打开方式
        encoding : str
            存储时的编码方式

        Returns
        -------
        None.

        '''
        self.__csvFile = open(fileAddr,fileOperateType)
        self.__csvName = fileAddr
        self.__encodingMethod = encoding
    
    
    def writerow(self,rowData):
        '''
        向csv文件写入一行数据

        Parameters
        ----------
        rowData : list of string
            要写入的字符串列表

        Returns
        -------
        None.

        '''
        writeData = str()
        for now in rowData:
            writeData += str(now)
            writeData += ','
        writeData = writeData[:-1]+'\n'
        self.__csvFile.write(writeData.encode(self.__encodingMethod))
        
    def __del__(self):
        '''
        默认析构函数

        Returns
        -------
        None.

        '''
        self.__csvFile.close()
        