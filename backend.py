# coding=utf-8
#!/usr/bin/env python

import datetime;
import xlrd
from xlutils.copy import copy
from xlrd import open_workbook


class RecordClient():
    AskUserIdString = "请输入员工号\n"
    
    #这里定义员工号和员工姓名 a1是员工号，周星驰是员工姓名
    UserDict = dict(a1="周星驰",a2="梁朝伟",a3="猪八戒",a4="孙悟空")

    #这里定义几个班，早中晚
    ShiftDict = dict(Morning="早班",Middle="中班",Night="晚班")

    #这里定义条形码组合
    MPdict = dict(a777888=("机器1","脸盆"),a999000=("机器2","牙膏"))

    #这里定义要输入的参数。这些参数会在excel的关键字行里被搜索并填入
    ParmDict = {"上机数":0,"接班模数":0,"交班模数":0,"每模数":0}

    #这里定义输出excel文件
    FileName = "c:\Documents and Settings\Administrator\桌面\Book1.xls"

    #这里定义输出到excel文件第几个sheet(第一页为0)
    OutFileSheetNumber = 0
    
    #这里定义关键字行是哪一行(excel中的第二行是 1)
    OutFileKeyRowNumber = 1
        
    def __init__(self):
        #do some init..
        pass

    #Get username via userid
    def getUserId(self):
        self.userid = raw_input(self.AskUserIdString).strip()
        return self.userid

    def getUserName(self,id):
        #ToDo: exception
        self.username = self.UserDict[id];
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
        self.MPbarcode = raw_input("Please Scan Barcode!\n\t").strip()
        print "\t\t====Get Barcode:"+self.MPbarcode+"====\n"
        return self.MPbarcode

    def getMachineAndProduct(self):
        (M,P) = self.MPdict[self.scanbarcode()]
        self.Machine = M
        self.Product = P
        return M,P

    def queryParms(self):
        for parm in self.ParmDict:
            self.ParmDict[parm] = raw_input("请输入"+parm+":\n\t")


    def updateDB(self):
            print "正在写入数据库.....\n"
            rb = open_workbook(self.FileName)
            sheet = rb.sheets()[self.OutFileSheetNumber]
            wb = copy(rb)
            row = wb.get_sheet(self.OutFileSheetNumber).row(rb.sheets()[self.OutFileSheetNumber].nrows)
            row.write(3,encode(self.username))
            row.write(2,encode(self.userid))
            row.write(4,encode(self.Product))
            row.write(5,encode(self.Machine))
            row.write(6,encode(self.shift))
            for parm in self.ParmDict:
                for col in range(sheet.ncols):
                    cellValue = sheet.cell(self.OutFileKeyRowNumber,col).value
                    print cellValue
                    print unicode(parm,'cp936')
                    if cellValue == unicode(parm,'cp936'):
                        print "found "+parm+"at"+str(col)
                        row.write(col,encode(self.ParmDict[parm]))

            #保存到文件
            wb.save(self.FileName)
            print "写入数据库完成！\n"
 
    def printViaPrinter(self):
            print "正在打印\n"
            print "打印完成请取票\n"

            
def encode(str):
    return unicode(str,'cp936')

def mainloop():
    while True :
        try:
            is_name_confirmed = False
            while is_name_confirmed == False:
                this = RecordClient()
                UserId = this.getUserId()
                UserName = this.getUserName(UserId)
                if raw_input("请确认姓名(是=y,不是=n)：" + UserName+"\n") == "y":
                    is_name_confirmed = True
                    
            is_MPS_confirmed = False
            while is_MPS_confirmed == False:         
                Machine, Product = this.getMachineAndProduct()
                print "=====请确认以下信息====="
                print "姓名" + UserName+"\n"
                print "机器号：" + Machine +"\n"
                print "产品：" + Product +"\n"
                Shift = this.calculateShift()
                print "班次" + Shift +"\n"
                if raw_input("(是=y)：" + UserName+"\n") == "y":
                    is_MPS_confirmed = True

            is_Parms_confirmed = False
            while is_Parms_confirmed == False:
                this.queryParms()
                print "=====请确认以下信息,你这次输入的是====="
                for each in this.ParmDict:
                    print each+":\t"+this.ParmDict[each];
                if raw_input("(正确=y)：" + UserName+"\n") == "y":
                    is_Parms_confirmed = True
            this.updateDB()
            this.printViaPrinter()

                
        #异常处理
        except Exception as excep1:
            print "Error found ! please mailto:mscame@gmail.com"
            print type(Exception)
            print excep1.args
            
        
if __name__ == '__main__':    
    mainloop()
    
    
    
