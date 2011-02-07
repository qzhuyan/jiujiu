# coding=utf-8
#!/usr/bin/env python

import datetime;
import xlrd
from xlutils.copy import copy
from xlrd import open_workbook
import sys, traceback
from frontEnd import FrontEnd
from config import JiuJiuConfig
import wx
import time

class RecordClient():
    AskUserIdString = "\n请输入员工号:\n"
    
    #这里定义员工号和员工姓名 a1是员工号，周星驰是员工姓名, 配置文件已支持
    UserDict = dict(a1="周星驰",a2="梁朝伟",a3="猪八戒",a4="孙悟空")

    #这里定义几个班，早中晚
    ShiftDict = dict(Morning="早班",Middle="中班",Night="晚班")

    #这里定义条形码组合
    MPdict = dict(a777888=("机器1","脸盆"),a999000=("机器2","牙膏"))

    #这里定义要输入的参数。这些参数会在excel的关键字行里被搜索并填入
    ParmDict = {"上机数":0,"接班模数":0,"交班模数":0,"每模数":0}

    #这里定义输出excel文件，配置文件已支持
    FileName = "c:\Documents and Settings\Administrator\桌面\Book3.xls"

    #这里定义输出到excel文件第几个sheet(第一页为0)
    OutFileSheetNumber = 0
    
    #这里定义关键字行是哪一行(excel中的第二行是 1)
    OutFileKeyRowNumber = 1
        
    def __init__(self):
        self.configData = JiuJiuConfig()
        self.FileName = self.configData.get_GLCvalue("OutPutTable").encode('cp936')
        self.UserDict = self.configData.get_parsed_worksheet('EmploreeTable')
        self.BarcodeTable = self.configData.get_parsed_worksheet('BarcodeTable')
        pass

    def gui_input(self,MSG,Title="UserInput"):
        if type(MSG) != u"aaa":
            MSG = unicode(MSG,'cp936')
        dialog = FrontEnd(Title,MSG,Config = self.configData)
        return unicode(dialog.queryUser(MSG))
    
    def ask_input(self,MSG,Title="UserInput"):
        return self.gui_input(MSG,Title)
        #return raw_input(MSG).strip()
        
    #Get username via userid
    def getUserId(self):
        self.userid = self.ask_input(self.AskUserIdString)
        return self.userid

    def getUserName(self,id):
        #ToDo: exception
        self.username = self.UserDict[id][1].encode('cp936')
        return self.username 

    def calculateShift(self):
        #这里定义如何计算班次
        #每天3班，8：00-16：00，16：00-24：00，24：00-8：00
        hour = datetime.datetime.now().hour
        if hour in range(9,17): #      9 <= hour <17
            self.shift = self.ShiftDict['Morning']
        if hour in range(17,24):#      17 <= hour <24
            self.shift =  self.ShiftDict['Middle']
        if hour in range(0,9):  #      0 <= hour <8
            self.shift =  self.ShiftDict['Night']

        return self.shift
        
    def scanbarcode(self):
        #Todo: add some timeout
        self.MPbarcode = str(self.ask_input("Please Scan Barcode!\n\t"))
        return self.MPbarcode

    def getMachineAndProduct(self):
        self.thisBarcode = self.scanbarcode()
        self.Product = self.BarcodeTable[self.thisBarcode][4].encode('cp936')
        self.Machine = self.BarcodeTable[self.thisBarcode][2].encode('cp936')
        return self.Machine, self.Product


    def queryParms(self):
        #Clean ParmDict
        self.ParmDict = dict()
        for parm in self.BarcodeTable[self.thisBarcode][5:]:
            if parm != "":
                parm = parm.encode('cp936')
                userinput = self.ask_input("请输入"+parm+":\n\t")
                self.ParmDict[parm] = userinput

    def time_now(self):
        return str(datetime.datetime.now())

    def updateDB(self):
            print "正在写入数据库.....\n"
            rb = open_workbook(self.FileName)
            sheet = rb.sheets()[self.OutFileSheetNumber]
            wb = copy(rb)
            row = wb.get_sheet(self.OutFileSheetNumber).row(rb.sheets()[self.OutFileSheetNumber].nrows)
            row.write(0,str(time.time()))
            row.write(1,encode(self.time_now().split('.')[0]))
            row.write(2,self.userid)
            row.write(3,encode(self.username))
            row.write(4,encode(self.Product))
            row.write(5,encode(self.Machine))
            row.write(6,encode(self.shift))
            
            for parm in self.ParmDict:
                for col in range(sheet.ncols):
                    cellValue = sheet.cell(self.OutFileKeyRowNumber,col).value
                    if cellValue == unicode(parm,'cp936'):
                        data = self.ParmDict[parm]
                        if type(data) == type(u"hh"):
                            writedata = data
                        else:
                            writedata = encode(data)
                        row.write(col,writedata)

            #保存到文件
            wb.save(self.FileName)
            print "写入数据库完成！\n"
 
    def printViaPrinter(self):
            print "正在打印\n"
            print "打印完成请取票\n"

            
def encode(str):
    return unicode(str,'cp936')

def mainloop():
    app = wx.PySimpleApp()    
    while True :
        try:
            is_name_confirmed = False
            while is_name_confirmed == False:
                this = RecordClient()
                UserId = this.getUserId()
                UserName = this.getUserName(UserId)
                is_name_confirmed = True
                is_name_confirmed = False
                if this.ask_input("请确认姓名(是=y,不是=n)：" + UserName+"\n") == "y":
                    is_name_confirmed = True
                    
            is_MPS_confirmed = True
            is_MPS_confirmed = False
            while is_MPS_confirmed == False:         
                Machine, Product = this.getMachineAndProduct()
                msg =  "=====请确认以下信息====="
                msg = msg+ "姓名: " + UserName+"\n"
                msg = msg +  "机器号：" + Machine +"\n"
                msg = msg + "产品：" + Product +"\n"
                Shift = this.calculateShift()
                msg = msg +  "班次: " + Shift +"\n"
                msg = msg + "(是=y)：" + UserName+"\n"
                if this.ask_input(msg) == "y":
                    msg = ""
                    is_MPS_confirmed = True

            is_Parms_confirmed = False
            while is_Parms_confirmed == False:
                this.queryParms()
                msg = "=====请确认以下信息,你这次输入的是=====\n"
                for each in this.ParmDict:
                    tmpV = this.ParmDict[each]
                    msg = msg + each +":"+str(tmpV)+"\n"
                print msg
                if this.ask_input(msg) == "y":
                    is_Parms_confirmed = True
            this.updateDB()
            this.printViaPrinter()

                
            #        异常处理
        except Exception as excep1:
            exceptionTraceback = sys.exc_info()
            print "Error found ! please mailto:mscame@gmail.com"
            traceback.print_exc(file=sys.stdout)
            input()
        
if __name__ == '__main__':    
    mainloop()
    
    
    
