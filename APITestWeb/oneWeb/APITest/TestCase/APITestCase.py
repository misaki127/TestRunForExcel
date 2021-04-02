#coding:utf-8
import time

from APITest.common.LoggerObj import *
from APITest.common.TestCase import *
from APITest.common.globeObj import *
from APITest.TestCase.globalVariable import globalVariable
from APITest.excelObj.ExcelCellObj import CellObj
from APITest.excelObj.ExcelFuc import *
from APITest.common import globeObj


def insertVariable(variableSep,data,variableDict):
    try:
        if data == None or data =='':
            return ''
        if variableSep in data and variableDict != {}:
            if variableSep == configObj.getOption('variableSep','CodeFileVaribleSep'):
                data=updateCodeVarible(data,variableDict,variableSep)
            else:
                data = updateVaribleForStr(data,variableDict,variableSep)

        return data
    except Exception as e:
        logging.info("插入变量数据失败："+str(e)+'\n')


def excelObjToTestCase(variableDict=[]):
    try:
        sheetObj = excelObj.getSheetByName(configObj.getOption('SheetName','testCaseSheetName'))
        # 获取测试用例sheet中是否执行该列对象
        isExecuteColumn = excelObj.getColumn(sheetObj,int(configObj.getOption("TestCaseTotal","testCase_isExecute")))
        isExecuteDict = {}
        isExecuteList = []
        isExecuteIndexDict = {}
        for idx, i in enumerate(isExecuteColumn[1:]):
            caseName = excelObj.getCellOfValue(sheetObj, rowNo=idx + 2, colsNo=int(configObj.getOption("TestCaseTotal","testCase_testStepSheetName"))).strip()
            if i.value == None or i.value =='':
                i.value = 'n'
            if i.value.strip().lower() == 'y':
                isExecuteList.append(caseName)
                isExecuteIndexDict[caseName] = idx+1
        logging.info("需要执行的用例表名称为："+str(isExecuteList)+'\n')
        for k in isExecuteList:
            TestCaseList = getTestCase(k,variableDict)
            isExecuteDict[k] = TestCaseList
        return isExecuteDict,isExecuteIndexDict
    except Exception as e:
        logging.info("获取执行数据失败："+str(e)+'\n')


#读取sheet表，获取数据并储存在TestCase实例中，一行数据一个TestCase实例
def getTestCase(stepSheetName,variableDict):
    # global variableDict
    try:
        globalDict = globalVariable()
        caseStepObj = excelObj.getSheetByName(stepSheetName)
        stepNums = excelObj.getRowsNumber(caseStepObj)

        TestCaseList = []
        for index in range(2, stepNums + 1):

            stepRow = excelObj.getRow(caseStepObj, index)
            testCaseName = stepRow[int(configObj.getOption('TestCase','testCaseName')) - 1].value.strip()
            url = stepRow[int(configObj.getOption('TestCase','testUrl')) - 1].value.strip()
            try:
                # 检查url是否使用全局变量
                url = insertVariable(configObj.getOption('variableSep','globalVariableSep'),url,globalDict)
                # 检查是否有码变量
                url = insertVariable(configObj.getOption('variableSep','CodeFileVaribleSep'),url,globalDict)

            except Exception as e:
                logging.info("URL变量检测失败!" + str(e)+'\n')
            method = stepRow[int(configObj.getOption('TestCase','testMethod')) - 1].value.strip()
            sql = stepRow[int(configObj.getOption('TestCase','testSql')) - 1].value
            sqlVarible = stepRow[int(configObj.getOption('TestCase', 'testSqlVarible')) - 1].value
            try:
                if sql != None and sql != "":
                    # 检查sql是否使用全局变量
                    sql = insertVariable(configObj.getOption('variableSep','globalVariableSep'),sql,globalDict)
                    # 检查是否有码变量
                    sql = insertVariable(configObj.getOption('variableSep','CodeFileVaribleSep'),sql,globalDict)

                    variableDict_ext = sqlGetVarible(sql, sqlVarible,configObj.getOption('variableSep','sqlSeq'),configObj.getOption('variableSep','varibleSep'))

                    if variableDict_ext != None:
                        if variableDict != None:
                            variableDict.update(variableDict_ext)  # 将sql获得 的变量存入变量字典

            except Exception as e:
                logging.info("SQL变量检测失败!" + str(e)+'\n')

            dataType = stepRow[int(configObj.getOption('TestCase','testDataType')) - 1].value
            expectedResult = stepRow[int(configObj.getOption('TestCase','testExpectResult')) - 1].value

            data = stepRow[int(configObj.getOption('TestCase','testData')) - 1].value
            try:
                # 检查data是否使用全局变量
                data = insertVariable(configObj.getOption('variableSep','globalVariableSep'),data,globalDict)
                # 检查是否有码变量
                data = insertVariable(configObj.getOption('variableSep','CodeFileVaribleSep'),data,globalDict)

            except Exception as e:
                logging.info("Data变量检测失败!" + str(e)+'\n')
            headers = stepRow[int(configObj.getOption('TestCase','testHeaders')) - 1].value

            isToken = stepRow[int(configObj.getOption('TestCase','testIsToken')) - 1].value
            variable = stepRow[int(configObj.getOption('TestCase','testVariable')) - 1].value  # 需要传递的参数
            try:
                # 检查variable是否使用全局变量
                variable = insertVariable(configObj.getOption('variableSep','globalVariableSep'),variable,globalDict)
                # 检查是否有码变量
                variable = insertVariable(configObj.getOption('variableSep','CodeFileVaribleSep'),variable,globalDict)

            except Exception as e:
                logging.info("variable变量检测失败!" + str(e)+'\n')
            variableName = stepRow[int(configObj.getOption('TestCase','testVariableName')) - 1].value  # 需要传递的参数的命名

            waitTime = stepRow[int(configObj.getOption('TestCase','testWaitTime')) - 1].value  # 获取等待时间

            oneTestCase = TestCase(name=testCaseName,url=url,method=method,SQL=sql,SQLVariable=sqlVarible,
                                   dataType=dataType,expResult=expectedResult,data=data,headers=headers,
                                   isToken=isToken,findVariable=variable,nameVariable=variableName,waitTime=waitTime)

            TestCaseList.append(oneTestCase)
        return TestCaseList
    except IndexError:
        logging.info("模板缺少字段请检查是否为最新。"+'\n')
    except Exception as e:
        logging.info("获取TestCase类数据失败："+str(e)+'\n')


#通过一个TestCase实例发起请求，获取结果
def getResponseData(TestCaseObj,cookie):
    # global cookie
    try:
        TestCaseObj.toString()
        if TestCaseObj.headers == None or TestCaseObj.headers =="":
            if TestCaseObj.isToken == None or TestCaseObj.isToken == "" or TestCaseObj.isToken not in excelObj.getSheetNames():
                TestCaseObj.headers={}
            else:
                TestCaseObj.headers={'Cookie':cookie}
        else:
            if TestCaseObj.isToken == None or TestCaseObj.isToken == "" or TestCaseObj.isToken not in excelObj.getSheetNames():
                pass
            else:
                TestCaseObj.headers['Cookie'] = cookie
        if TestCaseObj.data == None:
            TestCaseObj.data = ""

        requestCode = 'getResponse(' + 'url="' + TestCaseObj.url + '",method="' + TestCaseObj.method + '",headers=' + str(TestCaseObj.headers) + ',' + TestCaseObj.data.replace("'", '"') + ')'
        logging.info("Request: " + requestCode+'\n')
        r = eval(requestCode)
        return r
    except Exception as e:
        logging.info("发起请求失败！"+str(e)+'\n')


# tokenName = ""
# cookie = ''
# variableDict = {}
# writeData = []

def run():
    # global tokenName,cookie,variableDict
    try:
        tokenName = ""
        cookie = ''
        variableDict = {}
        writeData = []

        ProjectStartTime = time.time()
        writeData.append(CellObj(index='B2',content=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),style=None,sheetName=configObj.getOption('SheetName','testReportSheetName')))
        sheetNameList = excelObj.getSheetNames()
        m = excelObjToTestCase(variableDict)
        runData =m[0]
        testCaseIndexDict = m[1]
        rows = 3
        ProPassed = 0
        ProFailed = 0
        ProErrored = 0

        for j,k in runData.items():  #遍历每一个需要执行的sheet表
            logging.info("开始执行 ‘{0}’ 测试用例".format(j)+'\n')
            variableDict = {}
            row = 1
            passed = 0
            failed = 0
            errored = 0
            caseStartTime = time.time()
            rows += 1
            pRows = rows
            writeData.append(CellObj(index='A'+str(rows),content=j,style=None,sheetName=configObj.getOption('SheetName','testReportSheetName')))
            for i in k:#遍历一个sheet表的每一行

                startTime = time.time()
                row +=1
                finallyResult = ''

                try:
                    isWaitting = True
                    variableDict_ext = {}
                    tokencheck = True
                    getTokenCount = 0
                    while tokencheck or isWaitting:
                        if getTokenCount > 3:
                            logging.info("获取token三次仍返回暂未登陆，请检查isToken填写是否正常！"+'\n')
                            finallyResult = "fail"
                            raise TimeoutError
                        tokenSheetName = i.isToken
                        if tokenSheetName in sheetNameList:
# ---------------------------token程序-------------------------------------------------------
                            if tokenName != tokenSheetName:
                                logging.info("进入获取token程序!"+'\n')
                                tokenCaseList = getTestCase(tokenSheetName,variableDict=variableDict)

                                oneCookie = ""
                                for case in tokenCaseList:   #遍历token表的每一行
                                    if case.headers == None or case.headers == '':
                                        case.headers={'Cookie':oneCookie}
                                    else:
                                        case.headers = eval(case.headers)
                                        case.headers['Cookie'] = oneCookie
                                    response = getResponseData(case,cookie)
                                    if response == None:
                                        logging.info("获取Token请求失败！请检查数据正确性"+'\n')
                                        raise KeyError
                                    else:
                                        code = str(response.status_code)
                                        result = response.json()
                                        logging.info("result: " + str(result)+'\n')
                                        resultCode = str(result['state'])
                                        if code != '200' or resultCode != '200':
                                            logging.info("获取token失败！"+'\n')
                                            raise KeyError
                                        else:
                                            if "token" in str(result):
                                                oneCookie ='super-token='+ str(jsonGetInfo(str(result),"token","token",',',',')['token'] )  #获取token

                                cookie = oneCookie
                                tokenName = tokenSheetName

                                logging.info("获取token成功！token={0}".format(cookie) +'\n')

# --------------------------------------------------------------------------------------------------------
                        try:
                            logging.info('变量列表为：'+str(variableDict))
                            #查看是否有使用变量
                            i.url = insertVariable(configObj.getOption('variableSep','packVaribleSep'),i.url,variableDict)
                            i.SQL = insertVariable(configObj.getOption('variableSep', 'packVaribleSep'), i.SQL,variableDict)
                            i.data = insertVariable(configObj.getOption('variableSep', 'packVaribleSep'), i.data,variableDict)
                            i.findVariable = insertVariable(configObj.getOption('variableSep', 'packVaribleSep'), i.findVariable,variableDict)
                        except Exception as e:
                            logging.info("获取变量的值失败！" + str(e)+'\n')
                            raise Exception

                        response = getResponseData(i,cookie)
                        if response == None:
                            logging.info("请求失败！请检查参数是否正确！"+'\n')
                            finallyResult = "error"
                            result=''
                            code = ''

                            raise KeyError
                        elif '导出' in i.name:
                            logging.info('进入导出程序' + '\n')
                            filename = getImportInfo(response)
                            logging.info('导出数据已写入:' + filename + '\n')
                            tokencheck = False
                            finallyResult = 'success'
                            result = ''
                            code = str(response.status_code)
                        else:
                            code = str(response.status_code)
                            result = response.json()
                            logging.info("result: " + str(result)+'\n')
                            if 'state' in list(result.keys()):
                                resultCode = str(result['state'])
                            else:
                                resultCode = code

                            if resultCode == "401" or code == "401" or "您暂未登入" in str(result):
                                logging.info("token已失效，重新获取token!"+'\n')
                                getTokenCount +=1
                            # elif '导入' in i.name:
                            #     logging.info('进入导出程序'+'\n')
                            #     filename = getImportInfo(response)
                            #     logging.info('导出数据已写入:' + filename+'\n')
                            #     tokencheck = False

                            else:
                                tokencheck = False
                                if i.expResult =="" or i.expResult == None:
                                    if code=='200' and resultCode == '200':
                                        finallyResult = 'success'
                                    else:
                                        finallyResult='fail'
                                else:
                                    isPass = passTesting(str(result),i.expResult,configObj.getOption('variableSep','expectResultSep'))
                                    if isPass:
                                        finallyResult = "success"
                                    else:
                                        finallyResult = 'fail'
        # ----------------------查找变量程序---------------------------------------------------------------

                                if i.findVariable != None and i.findVariable != "" and i.nameVariable != None and i.nameVariable != "":
                                    variableNameList = i.nameVariable.strip().split(',')
                                    variableData = getVariableData(i.findVariable)
                                    logging.info('variableData:::'+str(variableData))
                                    if variableData[1] == {}:
                                        for m in range(len(variableData[0])):
                                            variableDict_ext[variableNameList[m]] = JsonGetValue(result,variableData[0][m])[0][variableData[0][m]]
                                    else:
                                        variableData_1 = JsonGetValue(result,variableData[0],search=variableData[1])
                                        logging.info("---------"+str(variableData_1))
                                        searchList = list(variableData[1].keys())
                                        for s in searchList:
                                            del variableData_1[0][s]
                                        for v in range(len(list(variableData_1[0].keys()))):
                                            variableDict_ext[variableNameList[v]] = variableData_1[0][list(variableData_1[0].keys())[v]]
                                    #(find dict)
                                    logging.info("-------:::"+str(variableDict_ext))


                                    #
                                    # if i.nameVariable != None and i.nameVariable != "":
                                    #     # onlyFirstVariable 检测
                                    #     onlyFirstVariableList = eval(configObj.getOption('findVariableSep','onlyFirstVariable'))
                                    #     if j in onlyFirstVariableList:  # 检测表名 是否为取第一个值
                                    #
                                    #         if row in onlyFirstVariableList[j]:
                                    #             variableDict_ext = jsonGetFirstInfo(result, i.findVariable, i.nameVariable,configObj.getOption('variableSep','varibleSep'),configObj.getOption('variableSep','varibleSep'))
                                    #         else:
                                    #             variableDict_ext = jsonGetInfo(result, i.findVariable, i.nameVariable,configObj.getOption('variableSep','varibleSep'),configObj.getOption('variableSep','varibleSep'))
                                    #     elif ":" in i.findVariable:  # 检测是否需要使用搜索功能
                                    #         variableDict_ext = jsonSearch(result, i.findVariable, i.nameVariable,configObj.getOption('variableSep','varibleSep'),configObj.getOption('variableSep','varibleSep'))
                                    #     else:  # 普通模式
                                    #         variableDict_ext = jsonGetInfo(result, i.findVariable, i.nameVariable,configObj.getOption('variableSep','varibleSep'),configObj.getOption('variableSep','varibleSep'))
                                if variableDict_ext != None:
                                    variableDict.update(variableDict_ext)
        # ----------------------------------------------------------------------------------------------------
                        #获取结束时间
                        endTime = time.time()
# --------------------等待成功-----------------------------------------------------
                        isWaitting = False
                        if i.waitTime == None or i.waitTime == '':
                            isWaitting = False
                        else:
                            isWaitting = True
                            try:
                                maxUserTime = int(i.waitTime.split(configObj.getOption('variableSep','waitTimeSep'))[0])
                                waitUserTime = int(i.waitTime.split(configObj.getOption('variableSep','waitTimeSep'))[1])
                                if maxUserTime <= 0:
                                    raise ValueError
                                if waitUserTime <= 0:
                                    waitUserTime = 1
                            except Exception as e:
                                isWaitting = False
                                logging.info("最大等待时间或间隔时间 输入错误，格式为：最大等待时间,间隔时间"+str(e)+'\n')
                        if isWaitting:
                            if finallyResult == 'fail':
                                maxTime = endTime - startTime
                                if maxTime < maxUserTime:
                                    logging.info("正在等待。。"+'\n')
                                    time.sleep(waitUserTime)
                                else:
                                    isWaitting = False
                            else:
                                isWaitting = False
# ------------------------------------------------------------------------------------
                except Exception as e:
                    errorInfo = "执行{0}失败！".format(i.name) + str(e)
                    logging.info("执行{0}失败！".format(i.name) + str(e)+'\n')
                    finallyResult = 'error'
                    # raise ValueError
                logging.info("{0}-用例执行结果：{1}".format(i.name,finallyResult)+'\n')
                #index = turnExcelIndex([row,int(configObj.getOption('TestCase','testRunResult'))])
                if finallyResult == 'success':
                    style = 'green'
                    passed +=1
                    errCellObj = CellObj(index=turnExcelIndex([row, int(configObj.getOption('TestCase', 'testErrorInfo'))]),content='', style='red', sheetName=j)
                    runResultCellObj = CellObj(index=turnExcelIndex([row,int(configObj.getOption('TestCase','testRunResult'))]),content='pass',style='green',sheetName=j)
                elif finallyResult == 'fail':
                    style = 'red'
                    failed +=1
                    errCellObj = CellObj(index=turnExcelIndex([row, int(configObj.getOption('TestCase', 'testErrorInfo'))]),content='', style='red', sheetName=j)
                    runResultCellObj = CellObj(index=turnExcelIndex([row, int(configObj.getOption('TestCase', 'testRunResult'))]),content='fail', style='red', sheetName=j)
                else:
                    errored +=1
                    style = 'red'
                    errCellObj = CellObj(index=turnExcelIndex([row,int(configObj.getOption('TestCase','testErrorInfo'))]),content=errorInfo,style='red',sheetName=j)
                    runResultCellObj = CellObj(index=turnExcelIndex([row, int(configObj.getOption('TestCase', 'testRunResult'))]),content='error', style='red', sheetName=j)
                writeData.append(errCellObj)
                writeData.append(runResultCellObj)
                timeCellObj = CellObj(index=turnExcelIndex([row,int(configObj.getOption('TestCase','testApiTime'))]),content=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime() )),style=None,sheetName=j)
                if result != None or result != '':
                    resultCellObj = CellObj(index=turnExcelIndex([row,int(configObj.getOption('TestCase','testApiResult'))]),content=str(result),style=None,sheetName=j)
                else:
                    resultCellObj = CellObj(index=turnExcelIndex([row, int(configObj.getOption('TestCase', 'testApiResult'))]),content='', style=None, sheetName=j)
                if resultCode != None or resultCode != '':
                    codeCellObj=CellObj(index=turnExcelIndex([row,int(configObj.getOption('TestCase','testResponseCode'))]),content=str(resultCode),style=style,sheetName=j)
                else:
                    if code != None or code != '':
                        codeCellObj = CellObj(index=turnExcelIndex([row, int(configObj.getOption('TestCase', 'testResponseCode'))]),content=str(code), style=style, sheetName=j)
                    else:
                        codeCellObj = CellObj(index=turnExcelIndex([row, int(configObj.getOption('TestCase', 'testResponseCode'))]),content='', style=style, sheetName=j)
                rows +=1

                writeData.append(CellObj(index='A'+str(rows),content=i.name,style=None,sheetName=configObj.getOption('SheetName','testReportSheetName')))
                writeData.append(CellObj(index='B'+str(rows)+":"+'E'+str(rows),content=finallyResult,style=style,sheetName=configObj.getOption('SheetName','testReportSheetName')))
                writeData.append(CellObj(index='F'+str(rows),content=str(result),style=None,sheetName=configObj.getOption('SheetName','testReportSheetName')))

                writeData.append(timeCellObj)
                writeData.append(resultCellObj)
                writeData.append(codeCellObj)
            caseEndTime = time.time()
            oneTimeCellObj = CellObj(index=turnExcelIndex(
                [testCaseIndexDict[j]+1, int(configObj.getOption('TestCaseTotal', 'testCase_runTime'))]),content=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), style=None,sheetName=configObj.getOption('SheetName', 'testCaseSheetName'))
            if len(k) == passed:
                passCellObj = CellObj(index=turnExcelIndex([testCaseIndexDict[j]+1, int(configObj.getOption('TestCaseTotal', 'testCase_testResult'))]),content='pass',style='green',sheetName=configObj.getOption('SheetName','testCaseSheetName'))
            else:
                passCellObj = CellObj(index=turnExcelIndex([testCaseIndexDict[j]+1, int(configObj.getOption('TestCaseTotal', 'testCase_testResult'))]),content='fail',style='red',sheetName=configObj.getOption('SheetName','testCaseSheetName'))
            timeTotalCellObj = CellObj(index=turnExcelIndex([testCaseIndexDict[j]+1, int(configObj.getOption('TestCaseTotal', 'testCase_times'))]),content=str(caseEndTime-caseStartTime),style=None,sheetName=configObj.getOption('SheetName','testCaseSheetName'))
            writeData.append(oneTimeCellObj)
            writeData.append(timeTotalCellObj)
            writeData.append(passCellObj)
            #写报告
            writeData.append(CellObj(index='B'+str(pRows),content=str(passed+errored+failed),style=None,sheetName=configObj.getOption('SheetName', 'testReportSheetName')))
            writeData.append(CellObj(index='C'+str(pRows),content=str(passed),style=None,sheetName=configObj.getOption('SheetName', 'testReportSheetName')))
            writeData.append(CellObj(index='D'+str(pRows),content=str(failed),sheetName=configObj.getOption('SheetName', 'testReportSheetName')))
            writeData.append(CellObj(index='E'+str(pRows),content=str(errored),sheetName=configObj.getOption('SheetName', 'testReportSheetName')))

            ProPassed = ProPassed + passed
            ProFailed = ProFailed + failed
            ProErrored = ProErrored + errored

        ProjectEndTime =time.time()
        writeData.append(CellObj(index='D2', content=str(ProjectEndTime-ProjectStartTime), style=None,sheetName=configObj.getOption('SheetName', 'testReportSheetName')))

        writeData.append(CellObj(index='F2',content='成功：{0}，失败：{1}，错误：{2}'.format(str(ProPassed),str(ProFailed),str(ProErrored)),sheetName=configObj.getOption('SheetName', 'testReportSheetName')))

        createReportSheet(writeData,configObj.getOption('SheetName','testReportSheetName'))

        excelObj.save()

        delOldCodeData(globeObj.CodeInfo)
    except KeyError :
        logging.info("解析响应数据失败！"+'\n')
    except ValueError:
        logging.info("数据配置错误，检查文件正确性！"+'\n')
    except Exception as e:
        logging.info("解析数据失败！" + str(e)+'\n')