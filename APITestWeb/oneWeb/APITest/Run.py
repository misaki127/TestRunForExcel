#coding:utf-8


from APITest.TestCase.APITestCase import *


def getRun(filePath):
    try:
        print(filePath)
        workBook = excelObj.loadWorkBook(filePath)
        #执行测试用例
        run()
        #检测报告文件是否过大  10MB
        checkReport()
        return 1
    except Exception as e:
        logging.info("执行接口自动化程序错误："+str(e))
        return 0


