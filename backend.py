# coding=utf-8
#!/usr/bin/env python

import datetime;

class RecordClient():
    AskUserIdString = "请输入员工号\n"
    UserDict = dict(a1="周星驰",a2="梁朝伟",a3="猪八戒",a4="孙悟空")
    ShiftDict = dict(Morning="早班",Middle="中班",Night="晚班")
    MPdict = dict(a777888=("机器1","脸盆"),a999000=("机器2","牙膏"))
    ParmDict = {"aa":0,"bb":0,"cc":0,"ee":0}
    
    def __init__(self):
        #do some init..
        pass

    #Get username via userid
    def getUserId(self):
        self.userid = raw_input(self.AskUserIdString).strip()
        return self.userid

    def getUserName(self,id):
        #ToDo: exception
        return self.UserDict[id];

    def calculateShift(self):
        #每天3班，8：00-16：00，16：00-24：00，24：00-8：00
        hour = datetime.datetime.now().hour
        if hour in range(9,17):
            return self.ShiftDict['Morning']
        if hour in range(17,23):
            return self.ShiftDict['Middle']
        if hour in range(0,9):
            return self.ShiftDict['Night']
        
    def scanbarcode(self):
        #Todo: add some timeout
        self.MPbarcode = raw_input("Please Scan Barcode!\n\t").strip()
        print "\t\t====Get Barcode:"+self.MPbarcode+"====\n"
        return self.MPbarcode

    def getMachineAndProduct(self):
        (M,P) = self.MPdict[self.scanbarcode()]
        return M,P

    def queryParms(self):
        for parm in self.ParmDict:
            self.ParmDict[parm] = raw_input("请输入"+parm+":\n\t")


    def updateDB(self):
            print "正在写入数据库.....\n"
            print "写入数据库完成！\n"
 
    def printViaPrinter(self):
            print "正在打印\n"
            print "打印完成请取票\n"

if __name__ == '__main__':
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
                    print each;
                if raw_input("(正确=y)：" + UserName+"\n") == "y":
                    is_Parms_confirmed = True
            this.updateDB()
            this.printViaPrinter()

                
        #异常处理
        except Exception as excep1:
            print "Error found ! please mailto:mscame@gmail.com"
            print type(Exception)
            print excep1.args
            
        
    
    
    
    
    
