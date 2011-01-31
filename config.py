#!/usr/bin/env python
# coding=utf-8
from xlrd import open_workbook
import xlrd
import sys 

#========Global==========#
ConfigFilePath = 'config.xls'
GlobalConfigSheetName = 'config'
GlobalDict = 'superdict'
#========Global==========#

class JiuJiuConfig():
    def __init__(self,filePath = 'config.xls',globalConfigSheetName = 'config'):
        self.glSheetName = globalConfigSheetName
        self.conFpath = filePath
        self.Configuration = self.parse_config_file(self.conFpath)

    def parse_config_file(self,File):
        This = dict()
        wb = open_workbook(File)
        self.superDict = self.parse_worksheet(wb,GlobalDict)
        self.globalconfig = self.parse_worksheet(wb,self.glSheetName)
        ##Translate Chinese Value name to  English Value Name
        for item in self.globalconfig.keys():
            if self.superDict.has_key(item) and self.superDict[item][1] == u'v':
                This[str(self.superDict[item][2])] = self.globalconfig[item]
        ##Parse Tables
        self.ParsedWorksheet = dict()
        for item in self.superDict.keys():
            if self.superDict[item][1] == "sheet":
                self.ParsedWorksheet[str(self.superDict[item][2])]=(self.parse_worksheet(wb,item))
        return This
            
    def parse_worksheet(self,WorkBook,Sheet):
        ThisDict = dict()
        dictSheet = WorkBook.sheet_by_name(Sheet)
        for row in range(dictSheet.nrows):
            Key = dictSheet.cell(row,0).value
            if Key != "":
                valueList=[]
                for col in range(dictSheet.ncols):
                    valueList.append(dictSheet.cell(row,col).value)
                ThisDict[Key] = valueList
        return ThisDict

    def get_value(self,key,sheet=""):
        try:
            if sheet == "":
                ReturnV =  self.Configuration[key]
            else:
                return self.ParsedWorksheet[sheet][key]
        except Exception as excep1:
            return ""
        
    def get_GLCvalue(self,key):
        if self.Configuration.has_key(key):
            PreReturn =  self.Configuration[key][2]
            if self.superDict.has_key(PreReturn):
                return self.superDict[PreReturn][2]
            else:
                return PreReturn
        ##TODO: use throw exception
        else:
            return ""

        
if __name__ == '__main__':
    ThisConfig = JiuJiuConfig(ConfigFilePath,GlobalConfigSheetName)
    print ThisConfig.Configuration
    print ThisConfig.ParsedWorksheet
    print ThisConfig.superDict

    if ThisConfig.get_value('nano') == "":
        print "get_value test 1 passed!"
    if ThisConfig.get_value(u'a1',sheet="EmploreeTable")[0] == u"a1":
        print "get_value test 2 passed!"
    if ThisConfig.get_GLCvalue("FullScreen") == u"yes":
        print "get_GLCvalue test 1 passed!"
    if ThisConfig.get_GLCvalue("OutPutTable").encode("cp936") == "c:\Documents and Settings\Administrator\×ÀÃæ\Book1.xls":
        print "get_GLCvalue test 2 passed!"
    else:
        print [ThisConfig.get_GLCvalue("OutPutTable").encode('cp936')]
    input()
    


    

    

    

