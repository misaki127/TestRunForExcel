#coding:utf-8
#author:wanghan

import configparser
from APITest.common.globeObj import *
from APITest.common.common import *
from APITest.common.LoggerObj import *

class TestCase():
    result = None
    runTime = None
    responseInfo = None
    responseCode = None
    errorInfo = None


    def __init__(self,name,url,method,dataType=None,data=None,headers=None,isToken=None,findVariable=None,nameVariable=None,SQL=None,
                 SQLVariable=None,expResult=None,waitTime=None):
        self.waitTime = waitTime
        self.expResult = expResult
        self.SQLVariable = SQLVariable
        self.SQL = SQL
        self.nameVariable = nameVariable
        self.findVariable = findVariable
        # self.data = data
        # self.dataType = dataType
        self.data = splitCode(dataType,data,configObj.getOption('variableSep','dataTypeSep'),configObj.getOption('variableSep','dataSep'))
        self.method = method.strip()
        self.url = url.strip()
        self.headers = headers
        self.isToken = isToken
        self.name = name.strip()
        if not self.url or not self.method or not self.name:
            nullValueList = [x for x,y in {"name":self.name,"url":self.url,"method":self.method}.items() if not y]
            for i in nullValueList:
                logging.info("{0}的值为空，此项为必填，请检查数据！".format(i)+'\n')

        if self.method:
            if self.method.lower() not in ['get','post','delete','put','head','options','patch']:
                logging.info("'method'字段输入错误，只能输入'get','post','delete','put','head','options','patch'其中之一。\n")

    def toString(self):
        logging.debug("测试用例属性：name:{0},url:{1},method:{2},data:{3},headers:{4},isToken:{5},findVariable:{6},nameVariable:{7},SQL:{8},SQLVariable:{9},expResult:{10},waitTime:{11}".format(self.name,
                                self.url,self.method,self.data,self.headers,self.isToken,self.findVariable,self.nameVariable,self.SQL,self.SQLVariable,self.expResult,self.waitTime)+'\n')








