#coding:utf-8
#author:wanghan


import configparser
from APITest.common.common import *

class configObj():
    def __init__(self):
        self.config = configparser.ConfigParser()

    def read(self,fileName):
        code = getFileCoding(fileName)
        self.config.read(fileName,encoding=code)
        self.fileObj = open(fileName,"r+",encoding=code)

    def getOption(self,section,key):
        return self.config.get(section,key)

    def getSections(self):
        return self.config.sections()

    def getOptions(self,section):
        #返回的数据格式为[(key,value),(key,value)]元组
        return self.config.items(section)

    def removeOptions(self,section,key):
        self.config.remove_option(section,key)


    def removeSection(self,section):
        self.config.remove_section(section)


    def addSection(self,section):
        self.config.add_section(section)


    def addOption(self,section,key,value):
        self.config.set(section,key,value)


    def writeData(self):
        self.config.write(self.fileObj)

