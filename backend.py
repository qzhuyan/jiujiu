# coding=utf-8
#!/usr/bin/env python

import datetime;
import xlrd
from xlutils.copy import copy
from xlrd import open_workbook
import sys, traceback
from frontEnd import FrontEnd
from config import JiuJiuConfig
from printer import print_in_paper
import wx
import time

class RecordClient():
    AskUserIdString = "\n������Ա����:\n"
    
    #���ﶨ��Ա���ź�Ա������ a1��Ա���ţ����ǳ���Ա������, �����ļ���֧��
    UserDict = dict(a1="���ǳ�",a2="����ΰ",a3="��˽�",a4="�����")

    #���ﶨ�弸���࣬������
    ShiftDict = dict(Morning="���",Middle="�а�",Night="���")

    #���ﶨ�����������
    MPdict = dict(a777888=("����1","����"),a999000=("����2","����"))

    #���ﶨ��Ҫ����Ĳ�������Щ��������excel�Ĺؼ������ﱻ����������
    ParmDict = {"�ϻ���":0,"�Ӱ�ģ��":0,"����ģ��":0,"ÿģ��":0}

    #���ﶨ�����excel�ļ��������ļ���֧��
    FileName = "c:\Documents and Settings\Administrator\����\Book3.xls"

    #���ﶨ�������excel�ļ��ڼ���sheet(��һҳΪ0)
    OutFileSheetNumber = 0
    
    #���ﶨ��ؼ���������һ��(excel�еĵڶ����� 1)
    OutFileKeyRowNumber = 1
        
    def __init__(self):
        self.configData = JiuJiuConfig()
        self.FileName = self.configData.get_GLCvalue("OutPutTable").encode('cp936')
        self.UserDict = self.configData.get_parsed_worksheet('EmploreeTable')
        self.BarcodeTable = self.configData.get_parsed_worksheet('BarcodeTable')
        self.DisplayMsgTable = self.configData.get_parsed_worksheet('DisplayMsgTable')
        self.ErrorMessage = self.configData.get_GLCvalue("ErrorPrint").encode('cp936')
        self.ConfirmMessage = self.configData.get_GLCvalue("ConfirmMessage").encode('cp936')
        self.QbgC_USRID = self.configData.get_GLCvalue('QbgC_USRID')
        self.QbgC_BCODE = self.configData.get_GLCvalue('QbgC_BCODE')
        self.QbgC_PARM = self.configData.get_GLCvalue('QbgC_PARM')
        self.ConfirmBoxSize = int(self.configData.get_GLCvalue('FinalConfirmBoxSize'))
        pass

    def gui_input(self,MSG,Title="UserInput",BgC="white",AnsBoxSize=10):
        if type(MSG) != u"aaa":
            MSG = unicode(MSG,'cp936')
        dialog = FrontEnd(Title,MSG,Config = self.configData,QbgC=BgC,AnsBoxSize=AnsBoxSize)
        UserReturn = dialog.queryUser(MSG)
        if UserReturn == "+":
            raise UserWantRestart(MSG)
        return unicode(UserReturn)
    
    def ask_input(self,MSG,Title="UserInput",QbgC="white",AnsBoxSize=10):
        return self.gui_input(MSG,Title,QbgC,AnsBoxSize=AnsBoxSize)
        #return raw_input(MSG).strip()

    def ask_input_and_confirm(self,Query,Title="UserInput",QbgC="white",AnsBoxSize=10):
        MSG = Query
        user_confirmed_value = ""
        while True:
            thisInput = self.ask_input(MSG,Title,QbgC=QbgC)
            if thisInput == "" and user_confirmed_value != "":
                return user_confirmed_value
            else:
                user_confirmed_value = thisInput
                MSG = Query + self.ConfirmMessage+str(thisInput) #only input numbers

    #Get username via userid
    def getUserId(self):
        self.userid = self.ask_input(self.AskUserIdString,QbgC=self.QbgC_USRID)
        print self.userid
        return self.userid

    def getUserName(self):
        is_name_corrected = False
        while not is_name_corrected:
            tmpId = self.getUserId()
            tmpId = check_and_format_id(tmpId)
            if self.UserDict.has_key(tmpId):
                is_name_corrected = True                    
        self.username = self.UserDict[tmpId][1].encode('cp936')
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
        self.MPbarcode = str(self.ask_input(self.username+"\n"+"��������뿨",QbgC=self.QbgC_BCODE))
        return self.MPbarcode

    def getMachineAndProduct(self):
        is_barcode_correct = False
        while not is_barcode_correct:
            self.thisBarcode = check_and_format_id(self.scanbarcode())
            if self.BarcodeTable.has_key(self.thisBarcode):
                is_barcode_correct = True
        self.Product = self.BarcodeTable[self.thisBarcode][4].encode('cp936')
        self.Machine = self.BarcodeTable[self.thisBarcode][2].encode('cp936')
        return self.Machine, self.Product

    def queryParms(self):
        #Clean ParmDict
        self.ParmDict = dict()
        for parm in self.BarcodeTable[self.thisBarcode][5:]:
            if parm != "":
                parm = parm.encode('cp936')
                userinput = self.ask_input("������"+parm+":\n\t",QbgC=self.QbgC_PARM)
                self.ParmDict[parm] = userinput

    def time_now(self):
        return str(datetime.datetime.now())

    def updateDB(self):
            print "����д�����ݿ�.....\n"
            rb = open_workbook(self.FileName)
            sheet = rb.sheets()[self.OutFileSheetNumber]
            wb = copy(rb)
            row = wb.get_sheet(self.OutFileSheetNumber).row(rb.sheets()[self.OutFileSheetNumber].nrows)
            row.write(0,self.dataTag)
            row.write(1,encode(self.Time))
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

            #���浽�ļ�
            wb.save(self.FileName)
            print "д�����ݿ���ɣ�\n"
 
    def printViaPrinter(self,data=""):
        print "���ڴ�ӡ\n"
        if data == "":
            data = self.dataTag + "\t"\
                   + str(self.userid)+ "\t"\
                   + self.username + "\t"\
                   + self.shift + "\t"\
                   + str(self.thisBarcode)
        #data = "��ӡ"
        print_in_paper(data)
        print "��ӡ�����ȡƱ\n"

def check_and_format_id(s):
    try: 
        float(s)
        return float(s)
    except ValueError:
        return s
            
def encode(str):
    return unicode(str,'cp936')

def mainloop():
    app = wx.PySimpleApp()
    this = RecordClient()
    while True :
        try:
            UserName = this.getUserName()
            Machine, Product = this.getMachineAndProduct()
            msg =  ""
            msg = msg +  "�����ţ�" + Machine +"\n"
            msg = msg + "��Ʒ��" + Product +"\n"
#            Shift = this.calculateShift()
#           msg = msg +  "���: " + Shift +"\n"
#            msg = msg + "" + UserName+"\n"
            if this.ask_input(msg,AnsBoxSize=this.ConfirmBoxSize) == "":
                msg = ""
            this.queryParms()
            msg = "=====��ȷ��������Ϣ,������������=====\n"
            this.Time = this.time_now().split('.')[0]
            msg = msg +  "����: " + this.Time +"\n"
            Shift = this.calculateShift()
            msg = msg +  "���: " + Shift +"\n"
            msg = msg +  "����: " + UserName +"\n"
            msg = msg +  "�����ţ�" + Machine +"\n"
            msg = msg + "��Ʒ��" + Product +"\n"
            for each in this.ParmDict:
                tmpV = this.ParmDict[each]
                msg = msg + each +":"+str(tmpV)+"\n"
            print msg
            if this.ask_input(msg,AnsBoxSize=this.ConfirmBoxSize) == "":
                is_Parms_confirmed = True
            this.dataTag = str(time.time())
            this.updateDB()
            this.ask_input("��ȡ��ӡ��",AnsBoxSize=this.ConfirmBoxSize)
            this.printViaPrinter(msg)
            #        �쳣����
        except UserWantRestart as UserRestart:
            print "User ask restart!"
            continue
        except Exception as excep1:
            exceptionTraceback = sys.exc_info()
            print "Error found ! please mailto:mscame@gmail.com"
            traceback.print_exc(file=sys.stdout)
            #TODO: show fault to user!
            dialog = FrontEnd("","",Config = this.configData)
            dialog.showInfo2User(this.ErrorMessage)

class UserWantRestart(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return self.value
    
        
if __name__ == '__main__':
    while True:
        mainloop()
    
    
    
