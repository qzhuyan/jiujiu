# coding=utf-8
#!/usr/bin/env python

import datetime;
import xlrd
from xlutils.copy import copy
from xlrd import open_workbook


class RecordClient():
    AskUserIdString = "������Ա����\n"
    
    #���ﶨ��Ա���ź�Ա������ a1��Ա���ţ����ǳ���Ա������
    UserDict = dict(a1="���ǳ�",a2="����ΰ",a3="��˽�",a4="�����")

    #���ﶨ�弸���࣬������
    ShiftDict = dict(Morning="���",Middle="�а�",Night="���")

    #���ﶨ�����������
    MPdict = dict(a777888=("����1","����"),a999000=("����2","����"))

    #���ﶨ��Ҫ����Ĳ�������Щ��������excel�Ĺؼ������ﱻ����������
    ParmDict = {"�ϻ���":0,"�Ӱ�ģ��":0,"����ģ��":0,"ÿģ��":0}

    #���ﶨ�����excel�ļ�
    FileName = "c:\Documents and Settings\Administrator\����\Book1.xls"

    #���ﶨ�������excel�ļ��ڼ���sheet(��һҳΪ0)
    OutFileSheetNumber = 0
    
    #���ﶨ��ؼ���������һ��(excel�еĵڶ����� 1)
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
        #���ﶨ����μ�����
        #ÿ��3�࣬8��00-16��00��16��00-24��00��24��00-8��00
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
            self.ParmDict[parm] = raw_input("������"+parm+":\n\t")


    def updateDB(self):
            print "����д�����ݿ�.....\n"
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

            #���浽�ļ�
            wb.save(self.FileName)
            print "д�����ݿ���ɣ�\n"
 
    def printViaPrinter(self):
            print "���ڴ�ӡ\n"
            print "��ӡ�����ȡƱ\n"

            
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
                if raw_input("��ȷ������(��=y,����=n)��" + UserName+"\n") == "y":
                    is_name_confirmed = True
                    
            is_MPS_confirmed = False
            while is_MPS_confirmed == False:         
                Machine, Product = this.getMachineAndProduct()
                print "=====��ȷ��������Ϣ====="
                print "����" + UserName+"\n"
                print "�����ţ�" + Machine +"\n"
                print "��Ʒ��" + Product +"\n"
                Shift = this.calculateShift()
                print "���" + Shift +"\n"
                if raw_input("(��=y)��" + UserName+"\n") == "y":
                    is_MPS_confirmed = True

            is_Parms_confirmed = False
            while is_Parms_confirmed == False:
                this.queryParms()
                print "=====��ȷ��������Ϣ,������������====="
                for each in this.ParmDict:
                    print each+":\t"+this.ParmDict[each];
                if raw_input("(��ȷ=y)��" + UserName+"\n") == "y":
                    is_Parms_confirmed = True
            this.updateDB()
            this.printViaPrinter()

                
        #�쳣����
        except Exception as excep1:
            print "Error found ! please mailto:mscame@gmail.com"
            print type(Exception)
            print excep1.args
            
        
if __name__ == '__main__':    
    mainloop()
    
    
    
