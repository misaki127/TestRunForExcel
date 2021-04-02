#coding:utf-8
from APITest.common.LoggerObj import *
from APITest.common.globeObj import *

def globalVariable():
    try:
        caseStepObj = excelObj.getSheetByName(configObj.getOption('SheetName','globalVariableSheetName'))

        stepNums = excelObj.getRowsNumber(caseStepObj)
        colNums = excelObj.getColsNumber(caseStepObj)
        DictGlobalVariable = {}
        if colNums != 2:
            logging.info("全局变量表内的数据不符合模板，请检查是否填写错误！"+'\n')
            raise ValueError

        for index in range(2, stepNums + 1):
            stepRow = excelObj.getRow(caseStepObj, index)
            key = stepRow[0].value
            value = stepRow[1].value
            if key=='':
                logging.debug("键的值必须不为空！"+'\n')
                raise ValueError
            elif key == None or value == None:
                pass
            else:
                DictGlobalVariable[key] = value

        return DictGlobalVariable
    except Exception as e:
        logging.info("getGlobalVariable error:"+str(e)+'\n')