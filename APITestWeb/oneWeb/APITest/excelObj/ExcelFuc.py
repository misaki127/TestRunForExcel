#coding:utf-8

from APITest.excelObj.ExcelObj import *
from APITest.excelObj.ExcelCellObj import *
from APITest.common.globeObj import *
from openpyxl.styles import Alignment, Font
from APITest.common.common import *
import string





def writeCell(cellObj):
    try:
        sheetName = cellObj.sheetName
        sheet = excelObj.getSheetByName(sheetName)
        if ":" in cellObj.index:
            excelObj.mergeCell(sheet=sheet,content=cellObj.content,coordinate=cellObj.index,style=cellObj.style)
        else:
            excelObj.writeCell(sheet=sheet,content=cellObj.content,coordinate=cellObj.index,style=cellObj.style)
    except Exception as e:
        logging.info("写入单元格失败：" + str(e)+'\n')


def writeCellList(cellObjList):
    try:
        for i in cellObjList:
            i.toString()
            writeCell(i)
    except Exception as e:
        logging.info("写入单元格列表失败："+str(e)+'\n')


def createReportSheet( data, testReportSheetName):
    # 初始化接口自动化报告
    try:
        sheetList = excelObj.getSheetNames()
        if testReportSheetName in sheetList:
            del excelObj.workbook[testReportSheetName]
        excelObj.workbook.create_sheet(title=testReportSheetName)
        reportSheet = excelObj.workbook[testReportSheetName]
        reportSheet['A1'].alignment = Alignment(horizontal='center', vertical='center')
        list1 = [
                 CellObj(index="A1:F1",content='接口自动化脚本测试报告',style=None,sheetName=testReportSheetName),
                 CellObj(index="A2", content='开始时间', style=None, sheetName=testReportSheetName),
                 CellObj(index="C2", content='耗时', style=None, sheetName=testReportSheetName),
                 CellObj(index="E2", content='结果', style=None, sheetName=testReportSheetName),
                 CellObj(index="A3", content='用例组名称/用例名称', style=None, sheetName=testReportSheetName),
                 CellObj(index="B3", content='总数', style=None, sheetName=testReportSheetName),
                 CellObj(index="C3", content='通过', style=None, sheetName=testReportSheetName),
                 CellObj(index="D3", content='失败', style=None, sheetName=testReportSheetName),
                 CellObj(index="E3", content='错误', style=None, sheetName=testReportSheetName),
                 CellObj(index="F3", content='结果信息/错误信息', style=None, sheetName=testReportSheetName)
                 ]
        data = data + list1
        writeCellList(data)

    except Exception as e:
        logging.info("写入报告失败:" + str(e)+'\n')



def turnExcelIndex(data):
    try:
        listE = [i for i in string.ascii_uppercase]
        if len(data) == 1:
            resultList = spiltMathAndEnglish(data)
            englishList = [k for k in resultList[0]]
            col = 0
            for p in englishList:
                col = col + listE.index(p)+1
            row = int(resultList[1])
            return [row,col]
        elif len(data) == 2:
            row = data[0]
            col = data[1]
            n = col // 26
            l = col % 26
            if n==0 and l != 0:
                result=listE[l-1]+str(row)
            elif n != 0 and l==0:
                result = listE[n-1]+'Z'+str(row)
            elif n != 0 and l != 0:
                result = listE[n-1]+listE[l-1]+str(row)
            else:
                raise KeyError
            return result
    except Exception as e:
        logging.info("转换坐标失败！"+str(e)+'\n')


