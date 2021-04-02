#coding:utf-8

from APITest.common.LoggerObj import *

class CellObj():
    def __init__(self,index=None,content=None,style=None,sheetName=None):
        self.index = index
        self.content = content
        self.style = style
        self.sheetName = sheetName

    def toString(self):
        logging.debug("单元格属性：index={0},content={1},style:{2},sheetName:{3}".format(self.index,self.content,self.style,self.sheetName)+'\n')

