#coding:utf-8



import sys,os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
#BASE_DIR = 'D:/GIT/Test/APITest'

from APITest.excelObj.ExcelObj import *
from APITest.common.ConfigObj import *



#获取excel对象
excelObj = ParseExcel()
#workBook = excelObj.loadWorkBook(BASE_DIR +  "/TestData/数字乡村接口自动化.xlsx")
#获取配置文件对象
configObj = configObj()
configObj.read(BASE_DIR +  "/config/test.cfg")
#储存用过的码信息，文件名和行号
CodeInfo = []


codePath = '/usr/testcase/TestCase'
casePath = '/usr/testcase/TestCase'

# codePath = 'D:/ONE'
# casePath = 'D:/ONE'
