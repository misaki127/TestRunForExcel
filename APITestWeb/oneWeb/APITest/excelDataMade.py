#<coding:utf-8>
import re


import string,openpyxl


def run(str, sep):
    try:
        l = str.split(sep)
        r = 0
        s = ''
        for i in l:

            # if r and not searchV:
            if r > 0:
                if r % 2 == 0:
                    s = s + sep +'"'
                elif r % 2 != 0:
                    s = s + '" ' +sep
            r += 1
            s = s + i
        return s
    except Exception as e:
        print(e)

file = 'D:/数字乡村.xlsx'
wb = openpyxl.load_workbook(file)
sheetNames = wb.sheetnames

print(sheetNames)
for i in [  '一村一码', '一户一码', '租户管理', '景点管理', '酒店管理', '一户一码码关联', '一户一码活动', '阳光村务', '数字党建', '村民积分', '信息发布', '数字乡村H5', '开化token', '开化清水鱼管理']:
    sheet = wb[i]
    maxRow = sheet.max_row
    for x in range(maxRow):
        p = sheet.cell(row=x+1,column=6).value
        print(p)
        if p == None:
            pass
        else:
            if '$$$' in p:
                p = run(p,'$$$')
            if '&&&' in p:
                p = run(p,'&&&')
            if '$$&&' in p:
                p = run(p,'$$&&')
        print(p)
        sheet.cell(row=x+1,column=6).value = p


wb.save(file)

wb.close()